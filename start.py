import urllib3
# Evito caida por SSL autofirmado
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


import gitlab
import sys
import logging
import json
import base64
from configparser import ConfigParser

from time import strftime




# Cargo archivo de configuración gitlab
gl = gitlab.Gitlab.from_config('gitlab',[r'python-gitlab.cfg'])

# Cargo archivo de configuracion mediante ConfigParser
config_object = ConfigParser()
config_object.read('python-gitlab.cfg')

config = config_object["programconfig"]


# Configuro los Logs
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=config["DEBUG_LEVEL"])
logger = logging.getLogger(__name__)



projectObject=""
groupObject=""

def getProjectById (projectID):
	global projectObject
	error=""
	try:
		projectObject = gl.projects.get(projectID)
		# [<Project id:340>, <Project id:196>, <Project id:187>, <Project id:169>, <Project id:121>, <Project id:92>]
	except Exception as e:
		logger.error(e)
		error="Error: " + str(e)
	else:
		logger.info("Se ha buscado correctamente el proyecto '%s'" % projectObject.name_with_namespace)
		pass
	finally:
		return error

def searchGroup (groupID):
	global groupObject
	error=""
	try:
		groupObject = gl.groups.get(groupID)
		# [<Project id:340>, <Project id:196>, <Project id:187>, <Project id:169>, <Project id:121>, <Project id:92>]
	except Exception as e:
		logger.error(e)
		error="Error: " + str(e)
	else:
		logger.info("Se ha buscado correctamente el proyecto '%s'" % groupObject)
		pass
	finally:
		return error

def updateGitlabCI (gitlab_file, branch):
	global projectObject
	error=""
	try:
		# Se lee el archivo de origen para comparar con destino
		filetobase64 = open(gitlab_file,"r").read()		
		base64InputFile = base64.b64encode(filetobase64.encode("UTF-8")).decode('ascii')
		# Se lee el archivo de destino
		f = projectObject.files.get(file_path=".gitlab-ci.yml", ref=branch)
		# Se comparan
		if f.content == base64InputFile:
			logger.info("El pipeline es el mismo en origen y destino")
		else:
			# Se carga pipeline
			f.content = open(gitlab_file).read()
			f.save(branch=branch, commit_message="Se actualiza pipeline en rama '"+branch+"'")
			logger.info("Se actualiza pipeline en repo '"+projectObject.web_url+"'")
		pass
	except Exception as e:
		logger.error(e)
		error="Error: " + str(e)
	else:
		logger.info("El archivo existe '%s'" % f.name)
		pass
	finally:
		return error


def createFile (gitlab_file, branch):
	global projectObject
	error=""
	try:
		newdata = {
			'branch': branch,
			'commit_message': "Se agrega pipeline en branch '"+branch+"'",
			'actions': [
				{
				'action': 'create',
				'file_path': ".gitlab-ci.yml",
				'content': open(gitlab_file).read(),
				}
			]
		}
		f = projectObject.commits.create(newdata)

	except Exception as e:
		logger.error(e)
		error="Error creando pipeline en destino: " + str(e)
	else:
		logger.info("Se ha creado correctamente el pipeline en repo '"+projectObject.web_url+"'")
		pass
	finally:
		return error


def searchProjectAndUpdate(gitlab_file, project_number, branch_name, projectNameJson=None):
	error=""
	try:
		retorno=getProjectById(project_number)
		if(retorno.find("Error: ")!=-1):
			raise retorno

		if projectNameJson != None:
			if(projectObject.name != projectNameJson):
				raise ValueError("El ID del proyecto no concuerda con el nombre del mismo")



		projectObject.branches.get(branch_name)

		# Se actualiza archivo. Si no existe, se crea
		retorno = updateGitlabCI(gitlab_file, branch_name)
		if(retorno.find("Error: 404")!=-1):
			createFile(gitlab_file, branch_name)
	except Exception as e:
		logger.error(e)
		if ("404 Branch Not Found" in str(e)):
			error="Error: El proyecto no posee rama: " + branch_name
		elif ("El ID del proyecto" in str(e)):
			error="Error: El ID del proyecto no concuerda con el nombre del mismo. Revisar archivo cargado"
	finally:
		return error


def main():

	# TYPE_UPDATE = individual
	if(config["TYPE_UPDATE"] == "individual"):
		searchProjectAndUpdate(config["CI_FILE_PATH"],config["PROJECT_NUMBER"],config["BRANCH_NAME"])

	# TYPE_UPDATE = group
	elif(config["TYPE_UPDATE"] == "group"):
		groups_ids = json.loads(config["GROUPS_ID"])
		for group_id in groups_ids:
			group_list = gl.groups.get(group_id)
			for project in group_list.projects.list(all=True):
				retorno = searchProjectAndUpdate(config["CI_FILE_PATH"],project.id,config["BRANCH_NAME"])
				if(retorno.find("Error: ")!=-1):
					logger.error("Ha ocurrido un error para proyecto '%s': %s " % (project.web_url,retorno))

	# TYPE_UPDATE = file
	elif(config["TYPE_UPDATE"] == "file"):
		with open(config["FILE"]) as json_file:
			data = json.load(json_file)
		for number,project in data.items():
			retorno = searchProjectAndUpdate(config["CI_FILE_PATH"],number,config["BRANCH_NAME"],project)
			if(retorno.find("Error: ")!=-1):
				logger.error("Ha ocurrido un error para proyecto '%s': %s " % (project,retorno))




if __name__ == "__main__":
	main()
