# skeleton borrowed from Apache Beam's wordcount_minimal.py example

from __future__ import absolute_import

import argparse
import logging
import re

from past.builtins import unicode

import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions

def run(argv=None):
  """Main entry point; defines and runs the wordcount pipeline."""

  parser = argparse.ArgumentParser()
  parser.add_argument('--input',
                      dest='input',
                      default='gs://lswa-scalica/input/df_input.txt',
                      help='Input file to process.')
  parser.add_argument('--output',
                      dest='output',
                      default='gs://lswa-scalica/output/df_output.txt',
                      help='Output file to write results to.')
  known_args, pipeline_args = parser.parse_known_args(argv)
  pipeline_args.extend([
      '--runner=DataflowRunner',
      '--project=scalica-224416',
      '--staging_location=gs://lswa-scalica/staging',
      '--temp_location=gs://lswa-scalica/tmp',
      '--job_name=scalica-job',
  ])

  # We use the save_main_session option because one or more DoFn's in this
  # workflow rely on global context (e.g., a module imported at module level).
  pipeline_options = PipelineOptions(pipeline_args)
  pipeline_options.view_as(SetupOptions).save_main_session = True
  with beam.Pipeline(options=pipeline_options) as p:
    # format input into a dictionary
    def format_input(line):
        split_line = line.split(',')
        user_id = split_line[0]
        followees = split_line[1].split('-')            
        followees = [int(followee) for followee in followees if followee]
        followers = split_line[2].split('-')
        followers = [int(follower) for follower in followers if follower]

        return {
            'user_id': user_id, 
            'followees': followees, 
            'followers': followers
        }

    # split followees and followers into list of pairs
    def split(user_data):
        follower_pairs = []

        for followee in user_data['followees']:
            for follower in user_data['followers']:
                if followee != follower:
                    follower_pair = str(followee) + ',' + str(follower)
                    follower_pairs.append(follower_pair)
        
        return follower_pairs

    # emit a count for each follower_pair
    def map_count(follower_pair):
        return (follower_pair, 1)

    # format each follower pair + counter
    def format_result(map_pair):
        (follower_pair, count) = map_pair
        return '%s: %s' % (follower_pair, count)

    logging.info('reading from input')

    # Read the input file
    lines = p | ReadFromText(known_args.input)
    print(lines)

    suggestions = (
        lines
        | 'FormatInput' >> beam.Map(format_input)
        | 'Split' >> beam.FlatMap(split)
        | 'MapCount' >> beam.Map(map_count)
        | 'GroupAndSum' >> beam.CombinePerKey(sum))

    logging.info('generated suggestions')

    output = suggestions | 'Format' >> beam.Map(format_result)

    # for convenience, only write to one shard
    # for scalability, don't define this parameter so Dataflow scales numshards appropriately
    output | WriteToText(known_args.output, num_shards=1)

if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  run()
