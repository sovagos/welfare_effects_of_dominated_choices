class Contract:
    """A class representing a contract."""
    def __init__(self, contract_id):
        self.contract_id = contract_id
        self.program_id = None
        self.state_funded = None
        self.ranking = []
        self.scores_dic = {}
        self.capacity = 10**8
        self.cutoff = None
