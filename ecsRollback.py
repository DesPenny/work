#! /usr/bin/python
import boto3
import argparse
import sys
import json
import re

region = "ap-southeast-2"

ecs = boto3.client('ecs', region_name= region)

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--cluster", help="ECS Cluster", default="Prod")
parser.add_argument("-s", "--service", help="ECS Service Name", required=True)
parser.add_argument("-r", "--region", help="Define the Region - the default is ap-southeast-2")
parser.add_argument("-d", "--dryrun", help="Use -d to do a dry run")
parser.add_argument("-b", "--rollbackby", type=int, help=" rollback by n times")
parser.add_argument("-t", "--rollbackto", type=int, help="Rollsback to a certain revision number")

args = parser.parse_args()

revision = 0; # Sets revision as a global variable
n = 0
new_revision = 0


def get_running_revision():
        response = ecs.describe_services(cluster=args.cluster, services=[args.service])
        global revision
        get_list = response['services'][0]
        get_string = get_list['taskDefinition']
        re_obj = re.search(r"(\d+)$", get_string).group(0)
        revision = int(re_obj)
        return revision


def set_region():
	global region
	region = args.region
	return region


def rollback_by():
	global n
	n = args.rollbackby
	get_running_revision()
	global new_revision
	new_revision = revision - n
	return new_revision


def rollback_to():
	t = args.rollbackto
	get_running_revision()
	global new_revision
	new_revision = t
	return new_revision

def dryrun():
	get_revision()
	print "The current revision number is "+ str(revision)
	if args.rollbackby:
		rollback_by()
		print "You have chosen to rollback by "+str(n)+" revisions"
		print "The latest revision will be reverted back to revision number: " + str(new_revision)
	if args.rollbackto:
		rollback_to()
		print "You have chosen to roll back to revision " + str(new_revision)
	if args.region:
		print "The default region is set to " + region
		set_region()
		print "You are about to change the region to " + region 

def main():
	get_running_revision()
        print "Current revision is "+ str(revision)
        if args.rollbackby:
                new_revision = rollback_by()
                print "You have chosen to rollback by "+str(n)+" revisions"
                print "The latest revision will be reverted back to revision number: " + str(new_revision)
        elif args.rollbackto:
		new_revision = rollback_to()
                print "You have chosen to roll back to revision "+ str(new_revision)
	else:
		new_revision = revision - 1
		print "Rolling back to "+ str(new_revision)
	
	response = ecs.update_service(cluster=args.cluster,service=args.service,taskDefinition=(args.service+":"+str(new_revision)))
	
	

if __name__ == "__main__":
	main()

