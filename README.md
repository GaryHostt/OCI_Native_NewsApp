# OCI Native NewsApp
The app will gather &amp; store news CSVs for further analysis.

# Introduction

This API, app.py, receives GET requests that trigger pulling from [newsapi](https://newsapi.org/). The returned JSON is then written to csv files that are uploaded to an object storage bucket. The upload to the bucket is done by triggering an OCI-CLI shell script (newsupload & sourceupload). Lastly, the endpoint then deletes the csv files from local storage. 

This README also provides a 'Deployment Architecture', similar to a workshop. Different steps provide directions allowing for more general 'choose-your-own-adventure' implementation.

After building the [HubsterDB Flask API](https://github.com/GaryHostt/HubsterDatabase) in 2019, it's time to user containers so that I can deploy it on kubernetes instead of compute. 

***Continue below to see the pre-requisites, and go on to deploying your own flask API with a cloud native architecture!***

# Pre-requisites

### OCI CLI & docker
To begin developing on your macine, the [Oracle CLI](https://docs.cloud.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm) and [docker](https://docs.docker.com/install/) should both be installed, because the sh scripts in the repo rely upon this. Though, you could also implement this with the OCI Python SDK. You also have a working dockerfile & requirements.txt for the docker container. If not, start with step 0(a). 

### Existing flask API
You have an existing flask API with secret management similar to mine. A file just named 'apikey' that contains your newsapi.org key. Inspired by this [implementation](https://github.com/dylburger/reading-api-key-from-file/blob/master/Keeping%20API%20Keys%20Secret.ipynb). 

### Cron job
You have a cron job of some sort that can hit this API. After building the [DailyFrenchNewsTexter](https://github.com/GaryHostt/DailyNewsText), I made a new GO cron app that will hit my /api/news/csv endpoint once a day to generate my CSVs. This also needed to be containerized because it is [not recommended](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#each-container-should-have-only-one-concern) to run 2 different languages in one container, not because it can't be done, but architecturally each container should only have one conern.

[Click here to see the cron job that calls this API.](https://github.com/GaryHostt/GoChronCall)

### Optional: Configure email notification after CSV uploaded to bucket

Rather than implementing that in your API or cron code, [OCI can take care of notifying you](https://github.com/GaryHostt/OCI_DevOps/blob/master/Lab100.md).

# Outline & ToDo List

0: Flask API Containerization

1: upload containers to OCIR [verify directions]

2: create k8 cluster & deploy pod [create directions]

3: put API behind APIGW [link][screen if add auth]

4: put Health check on APIGW [screen]

implement:
ci/cd

Workshop Roadmap:
Part 2: Data catalog & data science - per pap not

Far road map:

Part X: deploy on compute
diff md

# Deployment

# Step 0: How to containerize your Python API.

## Creation of requirements.txt

If you haven't been using virtualenv like me and your 'pip freeze' command contains way more than your API needs - then you need to isolate your various requisite packagines. You can learn how to do the below steps [here](https://medium.com/python-pandemonium/better-python-dependency-and-package-management-b5d8ea29dff1):

1. Create a virtualenv 

2. Then try running your API 

3. see the requisite module missing

4. pip install it 

5. Repeat until you have a running API 

6. Then your pip freeze becomes the requirements.txtfile.

## Creation of dockerfile

This [guide](https://runnable.com/docker/python/dockerize-your-flask-application) is concise & helpful. 

This [guide](https://medium.com/@doedotdev/docker-flask-a-simple-tutorial-bbcb2f4110b5) also has some other details on getting started with docker.

## Helpful docker commands

Run this after you have your requirements.txt & dockerfile created.
```
cd /OCI_Native_NewsApp
docker build -t OCI_Native_NewsApp:latest .
docker run -d -p 80:80 OCI_Native_NewsApp:latest
docker ps
docker stop 145a2527107d3
```

# Route 1: Deploy your container 

## Upload your docker image to OCIR

Even though you have the OCI CLI configured, you need to configure your command line to interact with Oracle Container Repository. [This documentation](https://docs.cloud.oracle.com/en-us/iaas/Content/Registry/Tasks/registrypushingimagesusingthedockercli.htm) will show that and how to upload your image to the OCIR. [This workshop](https://www.oracle.com/webfolder/technetwork/tutorials/obe/oci/registry/index.html) provides extra screenshots for this process.

You can also [implement CI/CD in this process](https://blogs.oracle.com/shay/automating-cicd-for-docker-with-oracle-cloud-infrastructure-registry-and-developer-cloud-service).

## Deploying your container

To begin you'll need the infrastructure, you can get started [deploying nodes on OKE here](https://github.com/GaryHostt/OCI_DevOps/blob/master/Lab400.md)

After spinning up OKE, you will need to [pull your dockerfile from the registry](https://docs.cloud.oracle.com/en-us/iaas/Content/ContEng/Tasks/contengpullingimagesfromocir.htm?tocpath=Services%7CContainer%20Engine%7C_____12) to your OKE cluster. This [OKE & Registry lab](https://www.oracle.com/webfolder/technetwork/tutorials/obe/oci/oke-and-registry/index.html) can provide more context.

## Route 2: Run your apps natively in the Linux machine or on docker there

This may be the simpler and more familiar deploying method, especially for non-production instances.

# Troubleshooting

[How to activate/deactivate](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/)  your Python virtualenv

[Managing docker images & containers](https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes)

# Other Resources

The gold-standard cloud native app for OCI is of course, [MuShop](https://github.com/oracle-quickstart/oci-cloudnative).

# Life after Cloud

<p align="center">
  <img src="https://github.com/GaryHostt/OCI_Native_NewsApp/blob/master/markdown/screenshots/1.jpg?raw=true" alt="comic"/>
</p> 

[Source](http://www.commitstrip.com/en/2019/01/08/the-cloud-at-last/)


