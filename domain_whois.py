import argparse
import whois # python-whois


def get_args() -> argparse.Namespace:
    """Get all arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('--domain',
                        type=str,
                        help='Domain name for which to fetch information.')

    parser.add_argument('--type',
                        choices=['info', 'creation_date'],
                        default='info',
                        help='Specify the type of information to retrieve.')
    return parser.parse_args()


class DomainInfo:
    """A class for retrieving information about a domain, including creation date."""
    def __init__(self, domain_name: str):
        self.domain_name = domain_name

    def get_domain_info(self) -> whois.parser.WhoisIt:
        """Retrieve information about the domain using the whois service."""
        try:
            domain_info = whois.whois(self.domain_name)
            return domain_info
        except whois.WhoisCommandFailed as e:
            raise RuntimeError(f'Error fetching domain information: {str(e)}') from e

    def get_creation_date(self) -> str:
        """Get the creation date of the domain"""
        domain_info = self.get_domain_info()

        if isinstance(domain_info.creation_date, list):
            creation_date = domain_info.creation_date[0]
        else:
            creation_date = domain_info.creation_date

        return creation_date.strftime('%Y-%m-%d %H:%M:%S')


def main():
    '''Main function'''
    args = get_args()

    domain_info_instance = DomainInfo(args.domain)

    if args.type == 'info':
        domain_info = domain_info_instance.get_domain_info()
        print(f'Domain Info for {args.domain}:\n{domain_info}\n')
    elif args.type == 'creation_date':
        creation_date = domain_info_instance.get_creation_date()
        print(f'Creation Date for {args.domain}: {creation_date}')


if __name__ == '__main__':
    main()
