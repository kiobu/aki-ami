import json
import os

class MetadataParser:
    raw_metadata: any
    mod_dir: str
    metadata: dict

    def __init__(self, metadata_path: str):
        with open(metadata_path, 'r') as metadata:
            self.raw_metadata = json.load(metadata)
            self.mod_dir = os.path.dirname(os.path.realpath(metadata_path))

            # Do AMI metadata validations.
            self.validate_ami_format()
            self.validate_mod_types()
            self.validate_mod_paths()
            self.validate_server_mod_structure()

            # Set clean metadata to our raw metadata, since it's been successfully validated.
            self.metadata = self.raw_metadata['metadata']

    def validate_ami_format(self):
        try:
            assert type(self.raw_metadata['metadata']) is dict
            assert type(self.raw_metadata['metadata']['mods']) is list
        except (AssertionError, KeyError):
            raise MetadataInvalidException("Input is not in AMI format.")

    def validate_mod_types(self):
        try:
            for mod in self.raw_metadata['metadata']['mods']:
                assert mod['type'] in ('client', 'server')
        except (AssertionError, KeyError):
            raise MetadataModTypeInvalidException("AMI has invalid mod type(s).")

    def validate_mod_paths(self):
        try:
            for mod in self.raw_metadata['metadata']['mods']:
                assert all([os.path.exists(self.mod_dir + mod['path_to_root'])])
        except (AssertionError, KeyError):
            raise MetadataPathNotFoundException("Given AMI paths do not exist.")

    def validate_server_mod_structure(self):
        try:
            for mod in [mod for mod in self.raw_metadata['metadata']['mods'] if mod['type'] == 'server']:
                assert os.path.exists(self.mod_dir + mod['path_to_root'] + "/package.json")
        except (AssertionError, KeyError):
            raise MetadataServerModStructureInvalid("Missing package.json")


class MetadataInvalidException(Exception):
    """Metadata JSON is invalid or not in AMI structure."""


class MetadataPathNotFoundException(Exception):
    """Given mod path does not exist."""


class MetadataModTypeInvalidException(Exception):
    """Given mod type is not one of: 'client', 'server'."""


class MetadataServerModStructureInvalid(Exception):
    """Server mod structure is invalid (missing package.json)"""
