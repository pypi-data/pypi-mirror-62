import boto3
import cray.config as config
import cray.s3 as cs3
import subprocess

from os import getcwd
from shutil import copyfile
from pathlib import Path


def get_jobs(job_prefix=None):
    prefix = config.job_prefix() + "/"
    if job_prefix is not None:
        prefix = prefix + job_prefix
    return (
        (j.lstrip(config.job_prefix() + "/"))
        for j in cs3.list_subdirectories(config.bucket(), prefix)
    )


def job_file_prefix(jobID, file):
    return "{}/{}/{}".format(config.job_prefix(), jobID, file)


def get_ticket_jobs(ticket):
    return get_jobs(ticket)


def get_job_config(job):
    return cs3.load_json(
        config.bucket(), "{}/{}/config.json".format(config.job_prefix(), job)
    )


def is_job_cancelled(jobID):
    return cs3.file_exists(config.bucket(), job_file_prefix(jobID, "job_cancelled.zip"))


def is_job_active(jobID):
    return cs3.file_exists(config.bucket(), job_file_prefix(jobID, "job.zip"))


def exists(jobID):
    return is_job_active(jobID) or is_job_cancelled(jobID)


def cancel_job(jobID):
    s3 = boto3.resource("s3")
    jobZip = job_file_prefix(jobID, "job.zip")
    cancelledZip = job_file_prefix(jobID, "job_cancelled.zip")
    s3.Object(config.bucket(), cancelledZip).copy_from(
        CopySource="{}/{}".format(config.bucket(), jobZip)
    )
    s3.Object(config.bucket(), jobZip).delete()


def build_job_archive(
    tempdir, config_path, ssh_dir, fix_windows_path, docker_image, environment
):
    pwd = getcwd()
    if fix_windows_path:
        tempdir = tempdir.replace("\\", "/").replace("C:", "/c")
        pwd = pwd.replace("\\", "/").replace("C:", "/c")
        ssh_dir = ssh_dir.replace("\\", "/").replace("C:", "/c")

    if config_path != "":
        if Path(config_path).exists():
            copyfile(config_path, f"{pwd}/config.json")
        else:
            raise FileNotFoundError(f"No such configuration file: {config_path}")

    ssh_binding = ""
    if ssh_dir != "":
        ssh_binding = "-v {}:/root/.ssh:ro".format(ssh_dir)

    if environment:
        env_args = " ".join(f"-e {ei}" for ei in environment)
    else:
        env_args = ""

    cmd = "docker run -v {}:/build {} -v {}:/output {} --rm {}".format(
        pwd, ssh_binding, tempdir, env_args, docker_image
    )
    exit_code = subprocess.call(cmd, shell=True)
    if exit_code != 0:
        if env_args:
            # remove secrets
            cmd = "docker run -v {}:/build {} -v {}:/output {} --rm {}".format(
                pwd,
                ssh_binding,
                tempdir,
                " ".join(f"-e {ei.split('=')[0]}=..." for ei in environment),
                docker_image,
            )
        raise Exception(
            "'{}' submission failed: exited with code '{}'".format(cmd, exit_code)
        )


def submit_job_zip(zip_path, jobID):
    bucket = config.bucket()
    prefix = "{}/{}.zip".format(config.submit_prefix(), jobID)
    s3 = boto3.resource("s3")
    s3.meta.client.upload_file(zip_path, bucket, prefix)


def scheduled_at(jobID):
    return cs3.last_modified(config.bucket(), job_file_prefix(jobID, "config.json"))


def cancelled_at(jobID):
    if not is_job_cancelled(jobID):
        return None
    return cs3.last_modified(
        config.bucket(), job_file_prefix(jobID, "job_cancelled.zip")
    )
