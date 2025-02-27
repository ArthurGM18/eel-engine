-- ALL THIS HAS BEEN AUTOMATICALLY DONE BY SETUP.PY FOR AGES

-- Whole EelEngine Workspace: Acts as an umbrella for everything ---------------
workspace "EelEngine"

	configurations "Library"

	filter "system:linux"
		configurations "Executable"

	filter "system:windows"
		configuration "Library"

	filter {}
	objdir "!obj"

-- C Libraries that are used in Cython modules ---------------------------------

eelCLibraries = {
	eelCallbacks="src/eel/eelCallbacks",
	eelText="src/figure/eelText",
	eelShader="src/shader/eelShader"
}

for lib, libfiles in pairs(eelCLibraries) do

	project (lib)
		kind "StaticLib"
		files (libfiles .. ".*")

		filter "system:windows"
			links { "glfw3", "m", "freetype", "opengl32", "GLEW32" }

		filter "system:linux"
			links { "glfw", "m", "freetype", "GL", "GLEW", "SOIL" }

		filter {}

		targetdir "."
		pic "On"

		optimize "On"
		includedirs "/usr/include/freetype2"

end

-- Actual Engine: Either a Shared library or an executable ---------------------

project "Engine"
	kind "Makefile"

	filter "system:windows"
		buildcommands {
			"python setup.py build_ext --inplace --compiler=mingw64 -DMS_WIN64",
			"cp src/eel/eel.py eelengine/__init__.py",
			"mkdir -p eelengine/figure && mv eelengine/figure*pyd eelengine/figure",
			"cp src/figure/figure.py eelengine/figure/__init__.py"
		}
		cleanextensions ".pyd"

	filter "system:linux"
		buildcommands {
			"python3 setup.py build_ext --inplace",
			"cp src/eel/eel.py eelengine/__init__.py",
			"mkdir -p eelengine/figure && mv eelengine/figure*so eelengine/figure",
			"cp src/figure/figure.py eelengine/figure/__init__.py"
		}
		cleancommands {
			"rm -rf build obj eelengine",
			"rm *.a *.make Makefile",
			"rm src/eel/eel.c",
			"rm src/figure/figure.c",
			"rm src/gui/gui.c",
			"rm src/shader/shader.c"
		}

	filter {}

	buildmessage "Building the Engine"

--------------------------------------------------------------------------------
