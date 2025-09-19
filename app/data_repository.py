import logging
from typing import Optional

# from oci.identity import IdentityClient
# from oci.config import from_file
# from oci.auth.signers import InstancePrincipalsSecurityTokenSigner


class DataRepository:
    """
    Central repository for OCI IAM data.
    Handles initialization via tenancy profile or instance principal.
    Supports optional recursive traversal of compartments.
    """

    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)
        self.initialized = False
        self.profile_name: Optional[str] = None
        self.tenancy_ocid: Optional[str] = None
        self.use_instance_principal: bool = False
        self.recursive: bool = False

        # Placeholder data
        self.users = []
        self.policies = []
        self.groups = []

    def initialize(
        self,
        profile_name: Optional[str] = None,
        use_instance_principal: bool = False,
        recursive: bool = False,
    ):
        """
        Initialize the repository using either a profile or instance principal.
        """
        self.profile_name = profile_name
        self.use_instance_principal = use_instance_principal
        self.recursive = recursive

        if self.use_instance_principal:
            self.logger.info("Initializing repository with Instance Principal.")
            # signer = InstancePrincipalsSecurityTokenSigner()
            # self.client = IdentityClient(config={}, signer=signer)
        else:
            self.logger.info(f"Initializing repository with profile: {self.profile_name}")
            # config = from_file(profile_name=self.profile_name)
            # self.client = IdentityClient(config)

        # TODO: Fetch tenancy OCID, compartments, etc.
        self.initialized = True
        self.logger.info("DataRepository initialized successfully.")

    def load_users(self):
        """
        Load users for the tenancy.
        """
        if not self.initialized:
            raise RuntimeError("Repository not initialized. Call initialize() first.")

        # TODO: replace with OCI SDK call
        self.users = [
            {"id": "u1", "name": "Alice", "groups": ["Admins"]},
            {"id": "u2", "name": "Bob", "groups": ["Readers"]},
        ]
        self.logger.info(f"Loaded {len(self.users)} users.")
        return self.users

    def load_policies(self):
        """
        Load IAM policies for the tenancy.
        """
        if not self.initialized:
            raise RuntimeError("Repository not initialized. Call initialize() first.")

        # TODO: replace with OCI SDK call (with/without recursion)
        self.policies = [
            {
                "id": "p1",
                "name": "AdminPolicy",
                "statements": ["ALLOW group Admins to manage all-resources"],
            },
            {
                "id": "p2",
                "name": "ReadPolicy",
                "statements": ["ALLOW group Readers to read all-resources"],
            },
        ]
        self.logger.info(f"Loaded {len(self.policies)} policies.")
        return self.policies

    def load_groups(self):
        """
        Load groups for the tenancy.
        """
        if not self.initialized:
            raise RuntimeError("Repository not initialized. Call initialize() first.")

        # TODO: replace with OCI SDK call
        self.groups = [
            {"id": "g1", "name": "Admins"},
            {"id": "g2", "name": "Readers"},
        ]
        self.logger.info(f"Loaded {len(self.groups)} groups.")
        return self.groups

    def reset(self):
        """
        Reset repository to uninitialized state.
        """
        self.logger.info("Resetting repository state.")
        self.initialized = False
        self.profile_name = None
        self.use_instance_principal = False
        self.recursive = False
        self.users = []
        self.policies = []
        self.groups = []
