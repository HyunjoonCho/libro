#!/bin/bash

cd 'repos'
orgdir=$(pwd)
for bname in $(find . -mindepth 1 -maxdepth 1 -type d | sort -V); do
	cd ${orgdir}/${bname}
	bname=${bname#*/}

    if git tag | grep -q "D4J_${bname}_PRE_FIX_COMPILABLE"; then
        echo "${bname},already tagged"
        cd ${orgdir}
        continue
    fi

	# setup
	git reset --hard HEAD > /dev/null 2>&1
        git clean -df > /dev/null 2>&1
	git checkout D4J_${bname}_PRE_FIX_REVISION > /dev/null 2>&1
        git reset --hard HEAD > /dev/null 2>&1
        git clean -df > /dev/null 2>&1
        for ncfile in $(git diff D4J_${bname}_BUGGY_VERSION --name-only); do
                if [[ ${ncfile} == *"java"* ]]; then
                        continue
                fi
                git checkout D4J_${bname}_BUGGY_VERSION -- ${ncfile} 2> /dev/null
        done
        defects4j compile 2> /dev/null

	# if initially okay, return to loop
	if [[ $? -eq 0 ]]; then
		echo "${bname},ok"
		git commit -m "D4J_${bname}_PRE_FIX_COMPILABLE"
		git tag D4J_${bname}_PRE_FIX_COMPILABLE
		cd ${orgdir}
		continue
	fi

	# attempt to fix
	if [[ ${bname} == *"Jackson"* ]]; then
        for fname in $(git diff D4J_${bname}_BUGGY_VERSION --name-only | grep "PackageVersion"); do
            git checkout D4J_${bname}_BUGGY_VERSION -- ${fname}
        done
        rm src/test/java/com/fasterxml/jackson/databind/ext/TestSOAP.java
    fi
	if [[ ${bname} == *"Time"* ]] && (( $(ls -1 | wc -l) < 5 )); then
		mv defects4j.build.properties JodaTime
		mv .defects4j.config JodaTime
		cd JodaTime
	fi

	if [[ ${bname} == *"Lang"* ]]; then
	    rm -r src/java/org/apache/commons/lang/enum	
	    rm -r src/test/org/apache/commons/lang/enum	
	fi

    max_retries=5
    retry_count=0

    while [ $retry_count -lt $max_retries ]; do
        for fname in $(defects4j compile 2>&1 | grep -o "${bname}/.*\.java.*error" | grep -o "${bname}/.*\.java" | sort -u); do
            git checkout D4J_${bname}_BUGGY_VERSION -- ${fname#*/}
        done
        
        compile_output=$(defects4j compile 2>&1)
        
        if echo "$compile_output" | grep -q "Running ant (compile).*OK" && \
           echo "$compile_output" | grep -q "Running ant (compile.tests).*OK"; then
            break
        fi
        
        retry_count=$((retry_count + 1))
    done

	# report fix results
    defects4j compile > /dev/null 2>&1
	if [[ $? -eq 0 ]]; then
		echo "${bname},ok"
		git commit -m "D4J_${bname}_PRE_FIX_COMPILABLE"
        git tag D4J_${bname}_PRE_FIX_COMPILABLE
	else
		echo "${bname},fail"
	fi

	# restore state
	cd ${orgdir}
done
