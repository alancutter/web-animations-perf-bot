# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os


default_seconds_between_polls = 60 * 60

datetime_format = '%Y-%m-%dT%H:%M'
date_re = r'[\d-]{10}'
datetime_re = date_re + r'T[\d:]{5}'
commit_re = r'[\da-f]+'

build_url = 'http://commondatastorage.googleapis.com/chromium-browser-snapshots/'
index_url = build_url + '?prefix=Android/'
hosted_build_url_template = build_url + 'Android/%s/chrome-android.zip' # % commit
hosted_build_key_re = 'Android/(%s)/chrome-android\.zip' % commit_re
xmlns = 'http://doc.s3.amazonaws.com/2006-03-01'
list_cache_directory = 'list_cache'
commit_datetimes_path = os.path.join(list_cache_directory, 'commit_datetimes')
commit_position_tag = 'Cr-Commit-Position: refs/heads/master@{#%s}'

archive_directory = 'zips'
archived_build_file_template = archive_directory + '/Android-%s-%s.zip' # % (datetime, commit)
archived_build_file_inner_path = 'chrome-android/apks/ContentShell.apk'
extraction_directory = 'apks'
extracted_build_file_template = extraction_directory + '/ContentShell_%s_%s.apk' # % (datetime, commit)

run_benchmark_script = 'third_party/WebKit/PerformanceTests/Animation/PerfWeek/run-big-benchmarks.py'
all_results_directory = 'results'
results_directory_template = os.path.join(all_results_directory, '%s_%s_%s_%s') # % (datetime, commit, device, username)
results_filename = 'results.html'

spreadsheet_url = 'https://script.google.com/macros/s/AKfycbz16KoKbDyWVa9tFOTW09MYv7lSy8h3icmHKanO7FEmPgnz4TU/exec'
unwanted_test = 'telemetry_page_measurement_results.num_'
wanted_smoothness_tests = ['avg_surface_fps.', 'mean_frame_time.', 'jank_count.', 'max_frame_delay.']
results_directory_re = r'([\d-]{10})T\d\d:\d\d_([\da-f]+)_([\d\w]+)_(\w+)'
upload_datetime_format = '%Y-%m-%d %H:%M:%S'
