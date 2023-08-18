import argparse
import pandas as pd
from faker import Faker


def get_args() -> argparse.Namespace:
    """Get all arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--num_people', type=int,
                        default=10, help='number of fake people to generate')
    args = parser.parse_args()

    return args


def generate_fake_people(num_people):
    fake = Faker()

    data = {
        'name': [fake.name() for i in range(num_people)],
        'address': [fake.address() for i in range(num_people)],
        'country': [fake.country() for i in range(num_people)],
        'email': [fake.email() for i in range(num_people)],
        'phone': [fake.phone_number() for i in range(num_people)],
        'job': [fake.job() for i in range(num_people)],
        'birthdate': [fake.date_of_birth() for i in range(num_people)],
    }

    fake_df = pd.DataFrame(data)
    return fake_df


if __name__ == '__main__':
    args = get_args()
    fake_dataframe = generate_fake_people(args.num_people)

    print(fake_dataframe)
