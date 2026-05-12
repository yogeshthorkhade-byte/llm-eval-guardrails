import yaml


def load_policy():

    with open(
        "policies/policy.yaml",
        "r"
    ) as file:

        policy = yaml.safe_load(file)

    return policy