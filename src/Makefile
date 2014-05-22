glimmer_dir= #path to glimmer3.02 root directory

gf_classify: gfclassify.cc gfclassify.h build_glimmer copy_headers
	g++ -o gf_classify -Iincludes gfclassify.cc gfclassify.h glimmer_libs/libGLMicm.a glimmer_libs/libGLMcommon.a

build_glimmer:
	cd $(glimmer_dir)/src; make; cd -;cp $(glimmer_dir)/lib/*.a glimmer_libs/

copy_headers: 
	find $(glimmer_dir) -name '*.hh' -exec cp {} includes/ \;
