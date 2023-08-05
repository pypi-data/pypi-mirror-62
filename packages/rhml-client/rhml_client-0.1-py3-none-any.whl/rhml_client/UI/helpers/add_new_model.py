from rhythmic import rhythmicDB, faultReturnHandler;
from . import configuration, scanModelFolder;
from .packer import packFiles;
from os.path import exists, isdir as isDir, expanduser as expandUser;
from os import mkdir as makeDir;
from shutil import copyfile as copyFile;
from datetime import datetime;
from zipfile import ZipFile, ZIP_DEFLATED;

@faultReturnHandler
def addNewModel(model_name = None, model_dir = None):
    """
    addNewModel(model_name = None, model_dir = None, db_file_name = ".rhml_db.sqlite3")

    0. The path is checked to be already present in the database. If true, the according status returned, workflow stops.
    1. Model wrapper script template copied to the model's directory.
    2. The record containing model name, model path is added to `models_table`.
    3. The record of version 0 is added to `versions_table`.
    4. The model folder is scanned recursiveliy, adding all the files found to the `files_table` (absolute paths). 
    5. The `.rhml_storage` folder created within specified model directory.
    6. The initial, 0-version archive is created.

    """
    if model_dir == "~":
        model_path = expandUser(model_dir);
    else:
        model_path = model_dir;

    if ( (not model_name) or (not model_path) ):
        return "Can't add the model: model name or model path is missing."

    timestamp = str(datetime.now());
#####################################################33##########3#####
    templateSource = configuration.model_wrapper_class_file_name;
    templateDestination =  "{}/{}".format(model_path, configuration.model_wrapper_class_file_name);

    if not exists(templateDestination):
        copyFile(templateSource, templateDestination);
#######################################################################33
    #=================starting DB work =====================================

    with rhythmicDB(configuration.db_name, configuration.db_file_name) as db:

        probe = db.execute("SELECT model_name FROM models_table WHERE model_path = '{}'".format(model_path));

        if len(probe) > 0:
            return "The model [ {} ] stored in [ {} ] is already in the base.".format(probe[0][0], model_path);

        new_model_id = db.execute(
            """
            INSERT INTO models_table
            (
                model_name, 
                model_path, 
                last_version_timestamp
            ) 
            VALUES 
            (
                '{}', '{}', '{}'
            );
            """.format(model_name, model_path, timestamp));

        new_model_version_id = db.execute(
            """
            INSERT INTO versions_table
            (
                model_id,
                created_timestamp
            )
            VALUES
            (
                '{}', '{}'
            );
            """.format(new_model_id, timestamp));

        files_record_request = \
        """
        INSERT INTO files_table
        (
            model_version_id,
            absolute_path,
            last_modified_time
        )
        VALUES
        """;

        new_model_files = scanModelFolder(model_path);

        if len(new_model_files) > 0:
            files_record_values = "";

            for item_path in new_model_files:
                item = new_model_files[item_path];
                files_record_values += "('{}', '{}', '{}'), \n".format(new_model_version_id, item_path, item["last_modified_time"]);

            files_record_request += files_record_values[:len(files_record_values) -3] + ";"; #truncating `, \n` from the end of request and adding `;`.

            db.execute(files_record_request);

    #================= finished DB work =====================================

    model_storage_path = model_path + "/{}".format(configuration.storage_folder_name);

    if ( (not exists(model_storage_path)) or (not isDir(model_storage_path)) ):
        makeDir(model_storage_path);

    #================= Starting  building ver0 .zip in storage =====================================

    archive_name = model_storage_path + "/model_{}_ver0.zip".format(new_model_id);

    packFiles(model_path, archive_name, new_model_files);

    #================= Finished building ver0 .zip in storage =====================================

    return "Success";