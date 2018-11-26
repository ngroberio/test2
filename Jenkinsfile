#!groovy

// Run this pipeline on the custom Jenkins Slave ('jobtech-appdev')
// Jenkins Slaves have JDK and Maven already installed
// 'jobtech-appdev' has skopeo installed as well.
node('maven-appdev'){

  // The following variables need to be defined at the top level
  // and not inside the scope of a stage - otherwise they would not
  // be accessible from other stages.
  def version    = "1"

  // Set the tag for the development image: version + build number
  def devTag  = "${version}-${BUILD_NUMBER}"

  // Set the tag for the production image: version
  def prodTag = "p-${devTag}"

  // Checkout Source Code
  stage('Checkout Source') {
    checkout scm
  }

  // Call SonarQube for Code Analysis
  stage('Code Analysis') {
    echo "Running Code Analysis"

    // Replace xyz-sonarqube with the name of your Sonarqube project
    //sh "${mvnCmd} sonar:sonar -Dsonar.host.url=http://sonarqube-xyz-sonarqube.apps.$GUID.example.opentlc.com/ -Dsonar.projectName=${JOB_BASE_NAME}-${devTag}"
  }

  // Publish the built code file to Nexus
  stage('Publish to Nexus') {
    echo "Publish to Nexus"

    // Replace xyz-nexus with the name of your Nexus project
    //sh "${mvnCmd} deploy -DskipTests=true -DaltDeploymentRepository=nexus::default::http://nexus3.xyz-nexus.svc.cluster.local:8081/repository/releases"
  }

  // Build the OpenShift Image in OpenShift and tag it.
  stage('Build and Tag OpenShift Image') {
    echo "Building OpenShift container image sokapi:${devTag}"

   // Start Binary Build in OpenShift using the file we just published
   sh "oc delete dc sokapi -n jt-dev"
   sh "oc new-app jt-dev/sokapi:${devTag} --name=sokapi --allow-missing-imagestream-tags=true -n jt-dev"
   sh "oc set triggers dc/sokapi --remove-all -n jt-dev"

     // The filename is openshift-tasks.war in the 'target' directory of your current
     // Jenkins workspace
     //sh "oc start-build tasks --follow --from-file=./target/openshift-tasks.war -n jt-dev"

     // OR use the file you just published into Nexus:
     // sh "oc start-build sokapi --follow --from-file=http://nexus3.xyz-nexus.svc.cluster.local:8081/repository/releases/jobtehc/sokannonser/api/${version}/sokapi-${version}.war -n jt-dev"

     // Tag the image using the devTag
     openshiftTag alias: 'false', destStream: 'sokapi', destTag: devTag, destinationNamespace: 'jt-dev', namespace: 'jt-dev', srcStream: 'sokapi', srcTag: 'latest', verbose: 'false'
  }

  // Deploy the built image to the Development Environment.
  stage('Deploy to Dev Env') {
    echo "Deploying container image to Development Env Project"

    // Update the Image on the Development Deployment Config
    sh "oc set image dc/sokapi sokapi=docker-registry.default.svc:5000/jt-dev/sokapi:${devTag} -n jt-dev"

      // Update the Config Map which contains the users for the Tasks application
      //sh "oc delete configmap tasks-config -n jt-dev --ignore-not-found=true"
      //sh "oc create configmap tasks-config --from-file=./configuration/application-users.properties --from-file=./configuration/application-roles.properties -n jt-dev"

      // Deploy the development application.
      echo "[openshiftDeploy]"
      openshiftDeploy depCfg: 'sokapi', namespace: 'jt-dev', verbose: 'false', waitTime: '', waitUnit: 'sec'
      echo "[openshiftVerifyDeployment]"
      openshiftVerifyDeployment depCfg: 'sokapi', namespace: 'jt-dev', replicaCount: '1', verbose: 'false', verifyReplicaCount: 'false', waitTime: '15', waitUnit: 'sec'
      //echo "[openshiftVerifyDeployment]"
      //openshiftVerifyService namespace: 'jt-dev', svcName: 'sokapi', verbose: 'false', waitTime: '15', waitUnit: 'sec'
  }

  // Run Unit Tests on Development Environment.
  stage('Dev Env Unit Tests') {
    echo "Running Dev Unit Tests"
    // TBD
  }

    // Run Unit Tests on Development Environment.
  stage('Dev Env Integration Tests') {
    echo "Running Dev Integration Tests"
    // TBD
  }

   // Deploy the built image to the Test Environment.
  stage('Deploy to Test env') {
    echo "Deploying image to Test Env Project"

      // Update the Image on the Development Deployment Config
      sh "oc set image dc/sokapi sokapi=docker-registry.default.svc:5000/jt-dev/sokapi:${devTag} -n jt-test"

      // Deploy the test application.
      openshiftDeploy depCfg: 'sokapi', namespace: 'jt-test', verbose: 'false', waitTime: '', waitUnit: 'sec'
      openshiftVerifyDeployment depCfg: 'sokapi', namespace: 'jt-test', replicaCount: '1', verbose: 'false', verifyReplicaCount: 'false', waitTime: '', waitUnit: 'sec'
      //openshiftVerifyService namespace: 'jt-test', svcName: 'sokapi', verbose: 'false'
  }

 // Run Unit Tests on Test Environment.
  stage('Test Env Unit Tests') {
    echo "Running Test Env Unit Tests"
    // TBD
  }

  // Run Integration Tests on Test Environment.
  stage('Test Env Integration Tests') {
    echo "Running Test env Integration Tests"
    // TBD
  }

  // Copy Image to Nexus Docker Registry
  stage('Copy Image to Nexus Docker Registry') {
    echo "Copy image to Nexus Docker Registry"
    //sh "skopeo copy --src-tls-verify=false --dest-tls-verify=false --src-creds openshift:\$(oc whoami -t) --dest-creds admin:admin123 docker://docker-registry.default.svc.cluster.local:5000/jt-dev/sokapi:${devTag} docker://nexus-registry.nexus.svc.cluster.local:5000/sokapi:${devTag}"

    // Tag the built image with the production tag.
    //openshiftTag alias: 'false', destStream: 'sokapi', destTag: prodTag, destinationNamespace: 'jt-prod', namespace: 'jt-test', srcStream: 'sokapi', srcTag: devTag, verbose: 'false'
  }

  // A/B Deployment into Production
  // -------------------------------------
  // Do not activate the new version yet.
  def destApp   = "sokapi-a"
  def activeApp = ""

  stage('A/B Production Deployment') {
      input "Deploy to Production?"

      activeApp = sh(returnStdout: true, script: "oc get route sokapi -n jt-prod -o jsonpath='{ .spec.to.name }'").trim()
      if (activeApp == "sokapi-a") {
        destApp = "sokapi-b"
      }
      echo "Active Application:      " + activeApp
      echo "Destination Application: " + destApp

      // Update the Image on the Production Deployment Config
      sh "oc set image dc/${destApp} ${destApp}=docker-registry.default.svc:5000/jt-dev/sokapi:${devTag} -n jt-prod"

      // Update the Config Map which contains the users for the Tasks application
      //sh "oc delete configmap ${destApp}-config -n xyz-tasks-prod --ignore-not-found=true"
      //sh "oc create configmap ${destApp}-config --from-file=./configuration/application-users.properties --from-file=./configuration/application-roles.properties -n jt-prod"

      // Deploy the inactive application.
      openshiftDeploy depCfg: destApp, namespace: 'jt-prod', verbose: 'false', waitTime: '', waitUnit: 'sec'
      openshiftVerifyDeployment depCfg: destApp, namespace: 'jt-prod', replicaCount: '1', verbose: 'false', verifyReplicaCount: 'true', waitTime: '', waitUnit: 'sec'
      //openshiftVerifyService namespace: 'jt-prod', svcName: destApp, verbose: 'false'
  }

  stage('Switch over to new Version') {
    input "Switch Production?"

    echo "Switching Production application to ${destApp}."
    sh 'oc patch route sokapi -n jt-prod -p \'{"spec":{"to":{"name":"' + destApp + '"}}}\''
  }

}
