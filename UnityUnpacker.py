# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    UnityUnpacker.py                                   :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: vvaucoul <vvaucoul@student.42.Fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/03/23 11:08:05 by vvaucoul          #+#    #+#              #
#    Updated: 2023/03/23 11:08:05 by vvaucoul         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import os
import re
import tarfile
import gzip
import shutil
import argparse


class AssetDesc:
    def __init__(self):
        self.path = None
        self.asset_member = None
        self.meta_member = None


def unpack_unitypackage(input_file, output_path, nometa):
    with gzip.open(input_file, 'rb') as file_in:
        with open('temp.tar', 'wb') as file_out:
            shutil.copyfileobj(file_in, file_out)

    assets = {}

    with tarfile.open('temp.tar') as tar:
        for tarinfo in tar:
            fname = tarinfo.name

            asset_name = re.compile(r'([0-9a-f]+)', re.IGNORECASE)

            if not re.search(r'PaxHeader', fname, re.IGNORECASE) and asset_name.search(fname):
                asset_name = asset_name.search(fname).group(1)

                if asset_name not in assets:
                    assets[asset_name] = AssetDesc()

                a = assets[asset_name]

                if re.search(r'/asset$', fname, re.IGNORECASE):
                    a.asset_member = tarinfo
                elif re.search(r'/asset\.meta$', fname, re.IGNORECASE):
                    if not nometa:
                        a.meta_member = tarinfo
                elif re.search(r'/pathname$', fname, re.IGNORECASE):
                    a.path = tar.extractfile(tarinfo).read(
                        tarinfo.size).decode('utf-8').split('\n')[0]

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        for a in assets.values():
            if a.path is not None:
                print(f'Unpacking {a.path}')

                file_path = os.path.join(output_path, a.path)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)

                try:
                    if a.asset_member is not None:
                        with tar.extractfile(a.asset_member) as src_file:
                            with open(file_path, 'wb') as dst_file:
                                shutil.copyfileobj(src_file, dst_file)

                    if a.meta_member is not None:
                        with tar.extractfile(a.meta_member) as src_file:
                            with open(file_path + '.meta', 'wb') as dst_file:
                                shutil.copyfileobj(src_file, dst_file)

                except Exception as e:
                    print(f'Error unpacking {file_path} : {str(e)}')

    os.remove('temp.tar')


def main():
    parser = argparse.ArgumentParser(description='Unpack a UnityPackage file.')
    parser.add_argument('--nometa', action='store_true',
                        help="Don't unpack meta files")
    parser.add_argument('input_file', type=str,
                        help='Path to the UnityPackage file.')
    parser.add_argument('output_path', type=str,
                        help='Path to the output directory.')

    args = parser.parse_args()

    unpack_unitypackage(args.input_file, args.output_path, args.nometa)


if __name__ == '__main__':
    main()
