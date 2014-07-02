all: addons

design/law_tracking.xmi: design/law_tracking.zargo
	-echo "REBUILD law_tracking.xmi from law_tracking.zargo. I cant do it"

addons: law_tracking

law_tracking: design/law_tracking.uml
	xmi2oerp -r -i $< -t addons -v 2

clean:
	rm -rf addons/law_tracking/*
	sleep 1
	touch design/law_tracking.uml
