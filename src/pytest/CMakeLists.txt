set(test_files __init__.py
        test_version.py
        test_lymburn_repulsion.py
)

# Copy tests to the install directory.
install(FILES ${test_files}
        DESTINATION ${PYTHON_SITE_INSTALL_DIR}/${COMPONENT_NAME}/pytest
)

# Copy tests to the build directory for testing prior to installation.
copy_files_to_build("${test_files}" "hoomd-component-${COMPONENT_NAME}-pytest" "*.py")
