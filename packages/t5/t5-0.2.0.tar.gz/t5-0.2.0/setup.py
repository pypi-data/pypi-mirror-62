# Copyright 2020 The T5 Authors.
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

"""Install T5."""

import setuptools

# Get the long description from the README file.
with open('README.md') as fp:
  _LONG_DESCRIPTION = fp.read()

setuptools.setup(
    name='t5',
    version='0.2.0',
    description='Text-to-text transfer transformer',
    long_description=_LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Google Inc.',
    author_email='no-reply@google.com',
    url='http://github.com/google-research/text-to-text-transfer-transformer',
    license='Apache 2.0',
    packages=setuptools.find_packages(),
    package_data={
        '': ['*.gin'],
    },
    scripts=[],
    install_requires=[
        'absl-py',
        'allennlp',
        'babel',
        'gin-config',
        'mesh-tensorflow[transformer]>=0.1.10',
        'nltk',
        'numpy',
        'pandas',
        'rouge-score',
        'sacrebleu',
        'scikit-learn',
        'scipy',
        'sentencepiece',
        'six>=1.14',  # TODO(adarob): Remove once rouge-score is updated.
        'tensorflow-text==1.15.0rc0',
        'tfds-nightly',
    ],
    extras_require={
        'tensorflow': ['tensorflow==1.15'],
        'gcp': ['gevent', 'google-api-python-client', 'google-compute-engine',
                'google-cloud-storage', 'oauth2client'],
        'cache-tasks': [
            # TODO(adarob): Remove next line once avro-python3 is fixed.
            'avro-python3!=1.9.2',
            'apache-beam',
        ],
        'test': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            't5_mesh_transformer = t5.models.mesh_transformer_main:console_entry_point',
            't5_cache_tasks = t5.data.cache_tasks_main:console_entry_point'
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    keywords='text nlp machinelearning',
)
