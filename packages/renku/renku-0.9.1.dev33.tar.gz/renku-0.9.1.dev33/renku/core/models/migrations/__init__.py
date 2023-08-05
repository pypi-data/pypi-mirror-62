# -*- coding: utf-8 -*-
#
# Copyright 2017-2020 - Swiss Data Science Center (SDSC)
# A partnership between École Polytechnique Fédérale de Lausanne (EPFL) and
# Eidgenössische Technische Hochschule Zürich (ETHZ).
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
"""Renku JSON-LD migrations."""

from renku.core.models.migrations.dataset import migrate_absolute_paths, \
    migrate_dataset_file_id, migrate_dataset_schema, migrate_doi_identifier, \
    migrate_same_as_structure

JSONLD_MIGRATIONS = {
    'dctypes:Dataset': [migrate_dataset_schema, migrate_absolute_paths],
    'schema:Dataset': [
        migrate_absolute_paths, migrate_doi_identifier,
        migrate_same_as_structure, migrate_dataset_file_id
    ],
}
