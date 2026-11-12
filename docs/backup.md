# Backup

Second Brain can export and restore the knowledge database using JSON backup files.

Backups are useful before making larger changes to the knowledge base or when moving saved knowledge between installations.

## Export a backup

Open **Settings** and select the option to export the database.

Choose where the backup file should be saved.

Second Brain exports the stored knowledge to a JSON file.

The backup contains the saved knowledge entries and their associated metadata.

## Import a backup

Open **Settings** and choose the option to import a database backup.

Select a previously exported JSON file.

Second Brain validates the file before importing the knowledge.

Entries that already exist in the database may be skipped to avoid exact duplicates.

## Import results

After the import is complete, Second Brain reports:

- how many entries were imported
- how many entries were skipped

Skipped entries usually represent duplicates that were already present in the knowledge base.

## Invalid backup files

If the selected file is not a valid Second Brain backup, the import will be rejected.

Examples include:

- invalid JSON
- incorrect file structure
- missing required fields
- a missing backup file

The existing knowledge database is not intentionally replaced during this validation step.

## Recommended use

Create a backup:

- before deleting large amounts of knowledge
- before experimenting with major changes
- before moving the application to another computer
- regularly if the knowledge base contains important information

## Backup format

Second Brain currently uses JSON for database backups.

This makes the backup human-readable and allows the application to validate the structure before importing it.

## Restoring knowledge

Importing a backup adds valid entries to the current knowledge base.

It is therefore possible for some entries to be imported while duplicates are skipped.

After restoring a backup, you can open **View knowledge entries** to verify the imported information.