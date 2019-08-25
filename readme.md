- To use the generator, you must create a class and an entry in the config file

- The class name and the name in the config must match (generator can cast from CamelCase to snake_case automatically)

- The created class must implement two methods - `parse_tags()` and `gen_helper()`, which implement specific logic for each object

- As  data source are used .xml files. In the config, the `input` parameter can contain either a direct path to files or directories with files
