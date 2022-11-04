from typing import TypeVar, Any

from python.types import Input, Contract, Applicant, Application

T = TypeVar("T")


def correct_dominated_choices_lower(input: Input) -> Input:
    programs = _get_programs(contracts=input.contracts)
    return Input(
        contracts=input.contracts,
        applicants=[
            _get_corrected_applicant(
                programs=programs,
                contracts=_to_map_by_id(elements=input.contracts),
                applicant=applicant,
            )
            for applicant in input.applicants
        ],
    )


def _get_programs(contracts: list[Contract]) -> dict:
    programs: dict = {}
    for contract in contracts:
        program = programs.get(contract.program_id, {})
        program[
            "state_funded" if contract.state_funded else "self_funded"
        ] = contract.id
        programs[contract.program_id] = program
    return programs


def _get_corrected_applicant(
    programs: dict, contracts: dict[str, Contract], applicant: Applicant
) -> Applicant:
    ranked_applications: list[Application] = []
    for application in applicant.ranked_applications:
        if _has_ranked(
            contract_id=application.contract, ranked_applications=ranked_applications
        ):
            break
        contract = contracts[application.contract]
        if not contract.state_funded and _has_state_funded_pair(
            contract=contract, programs=programs
        ):
            state_funded_pair_contract_id = _get_state_funded_pair_contract_id(
                programs=programs, contract=contract
            )
            if not _has_ranked(
                contract_id=state_funded_pair_contract_id,
                ranked_applications=ranked_applications,
            ):
                if not _has_ranked(
                    contract_id=state_funded_pair_contract_id,
                    ranked_applications=applicant.ranked_applications,
                ):
                    ranked_applications.append(
                        Application(
                            contract=state_funded_pair_contract_id,
                            priority_score=application.priority_score,
                        )
                    )
                else:
                    ranked_applications.append(
                        _get_application_by_contract_id(
                            ranked_applications=applicant.ranked_applications,
                            contract_id=state_funded_pair_contract_id,
                        )
                    )
        ranked_applications.append(application)
    return Applicant(
        id=applicant.id,
        status=applicant.status,
        ranked_applications=ranked_applications,
    )


def _has_ranked(ranked_applications: list[Application], contract_id: str) -> bool:
    return 0 < len(
        [
            application
            for application in ranked_applications
            if application.contract == contract_id
        ]
    )


def _get_state_funded_pair_contract_id(programs: dict, contract: Contract) -> str:
    return programs[contract.program_id]["state_funded"]


def _has_state_funded_pair(programs: dict, contract: Contract) -> bool:
    return "state_funded" in programs[contract.program_id].keys()


def _get_application_by_contract_id(
    ranked_applications: list[Application], contract_id: str
) -> Any:
    for application in ranked_applications:
        if application.contract == contract_id:
            return application


def _to_map_by_id(elements: list[Contract]) -> dict[str, Contract]:
    return {element.id: element for element in elements}