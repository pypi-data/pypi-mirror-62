import configparser
import datetime as dt
import logging
import os
import sys
import traceback

import click
from htimeseries import HTimeseries

from haggregate import aggregate
from haggregate.regularize import regularize


@click.command()
@click.argument("configfile")
def main(configfile):
    """Create lower-step timeseries from higher-step ones"""

    # Start by setting logger to stdout; later we will switch it according to config
    logger = logging.getLogger("haggregate")
    stdout_handler = logging.StreamHandler()
    logger.addHandler(stdout_handler)

    try:
        config = configparser.ConfigParser()
        with open(configfile) as f:
            config.read_file(f)

        # Read the [General] section
        logfile = config.get("General", "logfile", fallback="")
        loglevel = config.get("General", "loglevel", fallback="warning")
        base_dir = config.get("General", "base_dir", fallback=".")
        target_step = config.get("General", "target_step")
        min_count = config.getint("General", "min_count")
        missing_flag = config.get("General", "missing_flag")
        target_timestamp_offset = config.get(
            "General", "target_timestamp_offset", fallback=None
        )

        # Remove [General] and make sure there are more sections
        config.pop("General")
        if not len(config.sections()):
            raise configparser.NoSectionError("No time series have been specified")

        # Setup logger
        logger.setLevel(loglevel.upper())
        if logfile:
            logger.removeHandler(stdout_handler)
            logger.addHandler(logging.FileHandler(logfile))

        # Log start of execution
        logger.info("Starting haggregate, " + dt.datetime.today().isoformat())

        # Read each section and do the work for it
        for section_name in config.sections():
            section = config[section_name]
            source_filename = os.path.join(base_dir, section.get("source_file"))
            target_filename = os.path.join(base_dir, section.get("target_file"))
            method = section.get("method")
            with open(source_filename, newline="\n") as f:
                ts = HTimeseries(f, format=HTimeseries.FILE)
            regts = regularize(ts, new_date_flag="DATEINSERT")
            aggts = aggregate(
                regts,
                target_step,
                method,
                min_count=min_count,
                missing_flag=missing_flag,
                target_timestamp_offset=target_timestamp_offset,
            )
            with open(target_filename, "w") as f:
                aggts.write(f, format=HTimeseries.FILE)

        # Log end of execution
        logger.info("Finished haggregate, " + dt.datetime.today().isoformat())

    except Exception as e:
        logger.error(str(e))
        logger.debug(traceback.format_exc())
        raise click.ClickException(str(e))


if __name__ == "__main__":
    sys.exit(main())
