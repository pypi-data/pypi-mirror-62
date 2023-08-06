import os
import argparse
import folderstats


def main():
    parser = argparse.ArgumentParser(
        description="Creates statistics from a folder structure")
    parser.add_argument(action='store',
        dest='folderpath',
        help='input folder path')
    parser.add_argument('-o', action='store',
        dest='output_filepath', default=None,
        help='output filepath, CSV and JSON supported',
        required=False)
    parser.add_argument('-c', action='store',
        dest='hash_name', default=None,
        help='hash function for checksum',
        required=False)
    parser.add_argument('-a', action='store_true',
        dest='absolute_paths', default=False,
        help='add absolute path column',
        required=False)
    parser.add_argument('-m', action='store_true',
        dest='microseconds', default=False,
        help='store timestamps with microseconds',
        required=False)
    parser.add_argument('-i', action='store_true',
        dest='ignore_hidden', default=False,
        help='ignore hidden files and folders, Linux and Unix only',
        required=False)
    parser.add_argument('-p', action='store_true',
        dest='parent', default=False,
        help='Add index and parent index',
        required=False)
    parser.add_argument('-v', action='store_true',
        dest='verbose', default=False,
        help='verbose console output',
        required=False)

    args = parser.parse_args()

    if not os.path.isdir(args.folderpath):
        print('Filepath is not a folder : ', args.folderpath)
        exit(-1)

    if args.output_filepath and \
        not args.output_filepath.endswith(('.csv', '.json')):
        print('Output type not supported : ', args.folderpath)
        exit(-1)

    df = folderstats.folderstats(args.folderpath,
                                 hash_name=args.hash_name,
                                 microseconds=args.microseconds,
                                 absolute_paths=args.absolute_paths,
                                 ignore_hidden=args.ignore_hidden,
                                 parent=args.parent,
                                 verbose=args.verbose)

    if args.output_filepath:
        if args.output_filepath.endswith('.csv'):
            df.to_csv(args.output_filepath, index=False)
        elif args.output_filepath.endswith('.json'):
            df.to_json(args.output_filepath, index=False)
    else:
        # Remove microseconds from timestamps
        for col in ['atime', 'mtime', 'ctime']:
            df[col] = df[col].apply(lambda d: d.replace(microsecond=0))

        # Print table to console
        print(','.join(df.columns))
        for row in df.itertuples(index=False, name=None):
            print(','.join(str(s) for s in row))


if __name__ == '__main__':
    main()
