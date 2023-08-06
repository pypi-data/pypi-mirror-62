# LCO Source Extraction Service CLI

# sep-service-caller
*Command line interface to LCO's source extraction service*

The source extraction service documentation can be found here: https://github.com/LCOGT/sextractor-service

## Installation
*pip install sep-service-caller*

## Logging
Logging is to STDOUT, with the ability to set the log level via the `--log-level` argument.

Extraction results are posted to LCO's Elasticsearch instance, and by default set to populate
the `source-extraction` index.

The `source-extraction` index can be [viewed in Kibana](http://kibana.lco.gtn/goto/8429a1c456dd20b653a4f1f8ef4ff78f).

## Usage
To view the help text, simply use the `-h` flag:

`sep-service -h`

```bash
usage: sep-service [-h] {file,dates} ...

Perform source extraction via the LCO source extraction service

positional arguments:
  {file,dates}  sep-service sub-commands
    file        Specify a basename to perform source extraction on
    dates       Specify a site/camera/date range to perform source extractions
                on.

optional arguments:
  -h, --help    show this help message and exit
```

The sep-service-caller has two sub-commands in order to facilitate two distict workflows:
* **file**: perform source extraction on a single file, specified by basename
* **dates**: perform source extraction on any number of files, specified by site/camera start and end date

Both commands accept the same optional parameters, allowing source extraction parameters to be provided. 

See LCO's [Source Extraction Service Docs](https://github.com/LCOGT/sextractor-service)

## Examples
Note: All examples include `<archive-auth-token>`, which should be replaced by an Archive API Token that has access
to the images that you wish to perform source extraction on.

### Solve by file
To view the help text for this subcommand, simply type `sep-service file -h`. This will show all of the
optional arguments available to you. Only a subset are showcased here.

To perform source extraction on a single file, `lsc1m005-fa15-20200214-0355-e91`
```bash
sep-service file lsc1m005-fa15-20200214-0355-e91 <archive-auth-token>
```

Let's try without DEFAULT values!
Note, that you must specify `--sep-mode CUSTOM` to override the sep service's [default values](https://github.com/LCOGT/sextractor-service#extraction-modes)
```bash
sep-service file lsc1m005-fa15-20200214-0355-e91 <archive-auth-token> --sep-mode CUSTOM --threshold 8.0
```
In this case, threshold will be set to 8.0, but all other tunable sep parameters will stay at their default

You can override as many values as you wish! Go crazy!
```bash
sep-service file lsc1m005-fa15-20200214-0355-e91 <archive-auth-token> --sep-mode CUSTOM --threshold 8.0 --min-area 2 --noise-model GLOBALRMS
```

### Solve by site/camera/date-range
To view the help text for this subcommand, simply type `sep-service dates -h`. This will show all of the
optional arguments available to you. Only a subset are showcased here.


To perform source extraction on all reduced science images (e91) from LSC/fa15 on DAY-OBS 20200214, 20200215, and 20200216:
```bash
sep-service dates lsc fa15 20200214 20200216 <archive-auth-token>
```

Let's try without DEFAULT values!
Note, that you must specify `--sep-mode CUSTOM` to override the sep service's [default values](https://github.com/LCOGT/sextractor-service#extraction-modes)
```bash
sep-service dates lsc fa15 20200214 20200216 <archive-auth-token> --sep-mode CUSTOM --deblend-n-threshold 24
```
In this case, like before, the number of deblending thresholds will be set to 24 but all other tunable sep parameters will stay at their default values.

You can override as many values as you wish.
```bash
sep-service dates lsc fa15 20200214 20200216 <archive-auth-token> --sep-mode CUSTOM --threshold 8.0 --min-area 2 --noise-model GLOBALRMS
```
