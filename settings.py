from selenium import webdriver

defaultEnvironment = "desa"
defaultDriver = "chrome"

environments={

    "desa" : {
        "driver" : "chrome",
        "baseURL" : "localhost",
        "port" : "19001",
        "SACLogin":{
            "baseURL" : "localhost",
            "port" : "18080",
            "user": "ccopello",
            "password": "Prisma2049"
        },
        "QAPI":{
            "baseURL" : "localhost",
            "port" : "10115"
        },
        "coreTx": {
            "baseURL": "localhost",
            "port": "10015"
        },
        "forms":{
            "baseURL":"localhost",
            "port":"9006"
        },
        "database": {
            "host":"localhost",
            "port":13306,
            "user":"spsT_usr",
            "passwd":"veef8Eed",
            "db":"sps433"
        },
        "requestBin":{
            "baseURL":"localhost",
            "port":"10113"
        }

    },

    "new_desa" : {
        "driver" : "chrome",
        "baseURL" : "localhost",
        "port" : "49001",
        "SACLogin":{
            "baseURL" : "localhost",
            "port" : "48080",
            "user": "ccopello",
            "password": "Prisma2043"
        },
        "QAPI":{
            "baseURL" : "localhost",
            "port" : "10115"
        },
        "coreTx": {
            "baseURL": "localhost",
            "port": "49000"
        },
        "forms":{
            "baseURL":"localhost",
            "port":"9006"
        },
        "database": {
            "host":"localhost",
            "port":13306,
            "user":"spsT_usr",
            "passwd":"veef8Eed",
            "db":"sps433"
        },
        "requestBin":{
            "baseURL":"localhost",
            "port":"10113"
        }

    },

    "local_machine" : {
        "driver" : "chrome",
        "baseURL" : "localhost",
        "port" : "30901",
        "SACLogin":{
            "baseURL" : "localhost",
            "port" : "30080",
            "user": "ccopello",
            "password": "Prisma2040"
        },
        "QAPI":{
            "baseURL" : "localhost",
            "port" : "10115"
        },
        "coreTx": {
            "baseURL": "localhost",
            "port": "30900"
        },
        "forms":{
            "baseURL":"localhost",
            "port":"30090"
        },
        "database": {
            "host":"localhost",
            "port":30306,
            "user":"spsT_usr",
            "passwd":"veef8Eed",
            "db":"sps433"
        }

    },
    
    "local_machine_mauro" : {
        "driver" : "chrome",
        "baseURL" : "localhost",
        "port" : "30901",
        "SACLogin":{
            "baseURL" : "localhost",
            "port" : "8080",
            "user": "ccopello",
            "password": "Prisma2044"
        },
        "QAPI":{
            "baseURL" : "localhost",
            "port" : "10115"
        },
        "coreTx": {
            "baseURL": "localhost",
            "port": "9002"
        },
        "forms":{
            "baseURL":"localhost",
            "port":"9004"	
        },
        "database": {
            "host":"localhost",
            "port":3306,
            "user":"root",
            "passwd":"root",
            "db":"sps433"
        },
        "requestBin":{
            "baseURL":"localhost",
            "port":"8000"
        }

    },

    "jenkins" : {
        "driver" : "headless_chrome",
        "baseURL" : "marathon-lb.infrastructure.marathon.mesos",
        "port" : "10001",
        "SACLogin":{
            "baseURL" : "marathon-lb.infrastructure.marathon.mesos",
            "port" : "10010",
            "user": "ccopello",
            "password": "Prisma2049"
        },
        "QAPI":{
            "baseURL" : "marathon-lb.infrastructure.marathon.mesos",
            "port" : "10115"
        },
        "coreTx":{
            "baseURL" : "marathon-lb.infrastructure.marathon.mesos",
            "port" : "10015"
        },
        "forms":{
            "baseURL":"marathon-lb.infrastructure.marathon.mesos",
            "port":"10116"
        },
        "database": {
            "host":"192.168.75.20",
            "port":3306,
            "user":"spsT_usr",
            "passwd":"veef8Eed",
            "db":"sps433"
        },
        "requestBin":{
            "baseURL":"marathon-lb.infrastructure.marathon.mesos",
            "port":"10113"
        }

    }
}

#environments ["jenkins"] = environments["desa"].copy()
#environments ["jenkins"]["baseURL"] = "marathon-lb.infrastructure.marathon.mesos"

