# BusinessOwner Retriever

Tool to retrieve list of Vietnamese registered business owners.

## Install

```
pip3 install businessowner-retriever
```

On Windows, you can download the prebuilt *msi* file, running it to install.

The software is primarily developed and tested on Ubuntu Linux. Windows 10 64-bit is rougly tested and provided installer. I don't have Mac OS X to support.

## Usage

The command name changes, depending on whether you installed the program.

Typical, it is `businessowner-retriever` on Linux and `businessowner-retriever.exe` on Windows.
If you run from the source, it is `businessowner_retriever.py`.

First, you can run the command with "--help" option to see summary of usage:


```sh
$ businessowner-retriever --help
Usage: businessowner-retriever [OPTIONS] COMMAND [ARGS]...

Options:
  -V, --version  Show the version and exit.
  -v, --verbose  Show more log to debug (verbose mode).
  --help         Show this message and exit.

Commands:
  businessowners  Get business owners
  codes           Get province, district codes
```

The program provides two subcommands, which you can also find brief usage guide:

```sh
$ businessowner-retriever codes --help
Usage: businessowner-retriever codes [OPTIONS] [AREA_CODE]

  Get province, district codes

Options:
  -v, --verbose  Show more log to debug (verbose mode).
  --help         Show this message and exit.
```

```sh
$ businessowner-retriever businessowners --help
Usage: businessowner-retriever businessowners [OPTIONS] AREA_CODE

  Get business owners

Options:
  -t, --tax-duty [normal|vat-exempted|suspended|closed|adjusting]
                                  [default: normal]
  -o, --out FILENAME              [required]
  -v, --verbose                   Show more log to debug (verbose mode).
  --help                          Show this message and exit.
```

Now are the steps:

### 1. Find province code

```sh
$ businessowner-retriever codes
┌───────────────────┬──────┐
│ Province          │ Code │
├───────────────────┼──────┤
│ An Giang          │ 805  │
│ Bà Rịa - Vũng Tàu │ 717  │
│ Bình Dương        │ 711  │
│ Bình Phước        │ 707  │
│ Bình Thuận        │ 715  │
│ Bình Định         │ 507  │
│ Bạc Liêu          │ 821  │
│ Bắc Cạn           │ 207  │
│ Bắc Giang         │ 221  │
│ Bắc Ninh          │ 223  │
│ Bến Tre           │ 811  │
│ Cao Bằng          │ 203  │
│ Cà Mau            │ 823  │
│ Cần Thơ           │ 815  │
│ Gia Lai           │ 603  │
│ Hà Giang          │ 201  │
│ Hà Nam            │ 111  │
│ Hà Nội            │ 101  │
│ Hà Tĩnh           │ 405  │
│ Hòa Bình          │ 305  │
│ Hưng Yên          │ 109  │
│ Hải Dương         │ 107  │
│ Hải Phòng         │ 103  │
│ Hậu Giang         │ 816  │
│ Khánh Hòa         │ 511  │
│ Kiên Giang        │ 813  │
│ Kon Tum           │ 601  │
│ Lai Châu          │ 302  │
│ Long An           │ 801  │
│ Lào Cai           │ 205  │
│ Lâm Đồng          │ 703  │
│ Lạng Sơn          │ 209  │
│ Nam Định          │ 113  │
│ Nghệ An           │ 403  │
│ Ninh Bình         │ 117  │
│ Ninh Thuận        │ 705  │
│ Phú Thọ           │ 217  │
│ Phú Yên           │ 509  │
│ Quảng Bình        │ 407  │
│ Quảng Nam         │ 503  │
│ Quảng Ngãi        │ 505  │
│ Quảng Ninh        │ 225  │
│ Quảng Trị         │ 409  │
│ Sóc Trăng         │ 819  │
│ Sơn La            │ 303  │
│ TP Hồ Chí Minh    │ 701  │
│ Thanh Hoá         │ 401  │
│ Thái Bình         │ 115  │
│ Thái Nguyên       │ 215  │
│ Thừa Thiên - Huế  │ 411  │
│ Tiền Giang        │ 807  │
│ Trà Vinh          │ 817  │
│ Tuyên Quang       │ 211  │
│ Tây Ninh          │ 709  │
│ Vĩnh Long         │ 809  │
│ Vĩnh Phúc         │ 219  │
│ Yên Bái           │ 213  │
│ Điện Biên         │ 301  │
│ Đà Nẵng           │ 501  │
│ Đắc Lắc           │ 605  │
│ Đắk Nông          │ 606  │
│ Đồng Nai          │ 713  │
│ Đồng Tháp         │ 803  │
└───────────────────┴──────┘
```

### 2. From the chosen province, lookup ward code

For example, we want to look into Đắk Nông province.

```
$ businessowner-retriever codes 606
┌──────────────────┬───────┐
│ District         │ Code  │
├──────────────────┼───────┤
│ Huyện Cư Jút     │ 60603 │
│ Huyện Krông Nô   │ 60605 │
│ Huyện Tuy Đức    │ 60617 │
│ Huyện Đắk Glong  │ 60615 │
│ Huyện Đắk Mil    │ 60607 │
│ Huyện Đắk R'Lấp  │ 60611 │
│ Huyện Đắk Song   │ 60609 │
│ Thị xã Gia Nghĩa │ 60613 │
└──────────────────┴───────┘
```

Try Cư Jút district, with code `60603`:

```
$ businessowner-retriever codes 60603
┌────────────────────┬─────────┐
│ Ward               │ Code    │
├────────────────────┼─────────┤
│ Thị trấn Ea T-Ling │ 6060301 │
│ Xã Cư Knia         │ 6060305 │
│ Xã Ea Pô           │ 6060303 │
│ Xã Nam Dong        │ 6060309 │
│ Xã Trúc Sơn        │ 6060315 │
│ Xã Tâm Thắng       │ 6060313 │
│ Xã Đắk DRông       │ 6060311 │
│ Xã Đắk Wil         │ 6060307 │
└────────────────────┴─────────┘

```

### 3. Retrieve list of business owners in that ward


```
$ businessowner-retriever businessowners 6060305 -o xa_cu_kinia.csv
Wrote to file: xa_cu_knia.csv
```

## Notes

- The server of data source, [www.gdt.gov.vn](http://www.gdt.gov.vn/wps/portal/home/hct), has access throttling. After an amount of data retrieval, it will block us. You should take a rest, before continuing, or finding a proxy to fake your IP address.

- On Windows, please run the program inside [ConEmu](https://conemu.github.io/). It is because *BusinessOwner Retriever* has an issue with character encoding in PowerShell console, which I (Quân) can't resolve (I'm just a Linux programmer).
