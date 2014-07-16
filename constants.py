default_seconds_between_polls = 60 * 60

datetime_format = '%Y-%m-%dT%H:%M'
date_re = r'[\d-]{10}'
datetime_re = date_re + r'T[\d:]{5}'
commit_re = r'[\da-f]+'

build_url = 'http://commondatastorage.googleapis.com/chromium-browser-continuous/'
index_url = build_url + '?prefix=Android/'
hosted_build_url_template = build_url + 'Android/%s/chrome-android.zip' # % commit
hosted_build_key_re = 'Android/(%s)/chrome-android\.zip' % commit_re
xmlns = 'http://doc.s3.amazonaws.com/2006-03-01'

archive_directory = 'zips'
archived_build_file_template = archive_directory + '/Android-%s-%s.zip' # % (datetime, commit)
archived_build_file_inner_path = 'chrome-android/apks/ContentShell.apk'
extraction_directory = 'apks'
extracted_build_file_template = extraction_directory + '/ContentShell-%s-%s.apk' # % (datetime, commit)

run_benchmark_script = 'third_party/WebKit/PerformanceTests/Animation/PerfWeek/run-big-benchmarks.py'
results_directory = 'results'
results_file_template = results_directory + '/result-%s-%s.html'
