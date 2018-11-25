#!groovy

// Run this pipeline on the custom Jenkins Slave ('jobtech-appdev')
// Jenkins Slaves have JDK and Maven already installed
// 'jobtech-appdev' has skopeo installed as well.
node{

  // Define Maven Command. Make sure it points to the correct
  // settings for our Nexus installation (use the service to
  // bypass the router). The file nexus_openshift_settings.xml
  // needs to be in the Source Code repository.
  //def mvnCmd = "mvn -s ./nexus_openshift_settings.xml"

  // Checkout Source Code
  stage('Checkout Source') {
    // TBD
    checkout scm
  }

  // The following variables need to be defined at the top level
  // and not inside the scope of a stage - otherwise they would not
  // be accessible from other stages.
  def version    = "t1"

  // Set the tag for the development image: version + build number
  def devTag  = "${version}-${BUILD_NUMBER}"
 
  // Set the tag for the production image: version
  def prodTag = "${version}"

  // Build Python Code
  stage('Build Python Code') {
    echo "Building version ${version}"

    // Command to build the code and skip tests
    //sh "${mvnCmd} clean package -DskipTests"
  }

  // Run the unit tests
  stage('Unit Tests') {
    echo "Running Unit Tests"
    // TBD
  }

  // Call SonarQube for Code Analysis
  stage('Code Analysis') {
    echo "Running Code Analysis"
    // TBD
    // Replace xyz-sonarqube with the name of your Sonarqube project
    //sh "${mvnCmd} sonar:sonar -Dsonar.host.url=http://sonarqube-xyz-sonarqube.apps.$GUID.example.opentlc.com/ -Dsonar.projectName=${JOB_BASE_NAME}-${devTag}"
  }

  // Publish the built code file to Nexus
  stage('Publish to Nexus') {
    echo "Publish to Nexus"
    // TBD
    // Replace xyz-nexus with the name of your Nexus project
    //sh "${mvnCmd} deploy -DskipTests=true -DaltDeploymentRepository=nexus::default::http://nexus3.xyz-nexus.svc.cluster.local:8081/repository/releases"
  }

  // Build the OpenShift Image in OpenShift and tag it.
  stage('Build and Tag OpenShift Image') {
    echo "Building OpenShift container image tasks:${devTag}"
   // TBD
   // Start Binary Build in OpenShift using the file we just published
     // The filename is openshift-tasks.war in the 'target' directory of your current
     // Jenkins workspace
     // Replace xyz-tasks-dev with the name of your dev project
     //sh "oc start-build tasks --follow --from-file=./target/openshift-tasks.war -n xyz-tasks-dev"

     // OR use the file you just published into Nexus:
     // sh "oc start-build tasks --follow --from-file=http://nexus3.xyz-nexus.svc.cluster.local:8081/repository/releases/org/jboss/quickstarts/eap/tasks/${version}/tasks-${version}.war -n xyz-tasks-dev"

     // Tag the image using the devTag
     //openshiftTag alias: 'false', destStream: 'tasks', destTag: devTag, destinationNamespace: 'xyz-tasks-dev', namespace: 'xyz-tasks-dev', srcStream: 'tasks', srcTag: 'latest', verbose: 'false'
  }

  // Deploy the built image to the Development Environment.
  stage('Deploy to Dev Env') {
    echo "Deploying container image to Development Env Project"
    // TBD
    // Update the Image on the Development Deployment Config
      //sh "oc set image dc/tasks tasks=docker-registry.default.svc:5000/xyz-tasks-dev/tasks:${devTag} -n xyz-tasks-dev"

      // Update the Config Map which contains the users for the Tasks application
      //sh "oc delete configmap tasks-config -n xyz-tasks-dev --ignore-not-found=true"
      //sh "oc create configmap tasks-config --from-file=./configuration/application-users.properties --from-file=./configuration/application-roles.properties -n xyz-tasks-dev"

      // Deploy the development application.
      // Replace xyz-tasks-dev with the name of your production project
      //openshiftDeploy depCfg: 'tasks', namespace: 'xyz-tasks-dev', verbose: 'false', waitTime: '', waitUnit: 'sec'
      //openshiftVerifyDeployment depCfg: 'tasks', namespace: 'xyz-tasks-dev', replicaCount: '1', verbose: 'false', verifyReplicaCount: 'false', waitTime: '', waitUnit: 'sec'
      //openshiftVerifyService namespace: 'xyz-tasks-dev', svcName: 'tasks', verbose: 'false'
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
    // TBD
    // Update the Image on the Development Deployment Config
      //sh "oc set image dc/tasks tasks=docker-registry.default.svc:5000/xyz-tasks-dev/tasks:${devTag} -n xyz-tasks-dev"

      // Update the Config Map which contains the users for the Tasks application
      //sh "oc delete configmap tasks-config -n xyz-tasks-dev --ignore-not-found=true"
      //sh "oc create configmap tasks-config --from-file=./configuration/application-users.properties --from-file=./configuration/application-roles.properties -n xyz-tasks-dev"

      // Deploy the development application.
      // Replace xyz-tasks-dev with the name of your production project
      //openshiftDeploy depCfg: 'tasks', namespace: 'xyz-tasks-dev', verbose: 'false', waitTime: '', waitUnit: 'sec'
      //openshiftVerifyDeployment depCfg: 'tasks', namespace: 'xyz-tasks-dev', replicaCount: '1', verbose: 'false', verifyReplicaCount: 'false', waitTime: '', waitUnit: 'sec'
      //openshiftVerifyService namespace: 'xyz-tasks-dev', svcName: 'tasks', verbose: 'false'
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
    // TBD
    //sh "skopeo copy --src-tls-verify=false --dest-tls-verify=false --src-creds openshift:\$(oc whoami -t) --dest-creds admin:admin123 docker://docker-registry.default.svc.cluster.local:5000/xyz-tasks-dev/tasks:${devTag} docker://nexus-registry.xyz-nexus.svc.cluster.local:5000/tasks:${devTag}"

    // Tag the built image with the production tag.
    // Replace xyz-tasks-dev with the name of your dev project
    //openshiftTag alias: 'false', destStream: 'tasks', destTag: prodTag, destinationNamespace: 'xyz-tasks-dev', namespace: 'xyz-tasks-dev', srcStream: 'tasks', srcTag: devTag, verbose: 'false'
  }

  // Blue/Green Deployment into Production
  // -------------------------------------
  // Do not activate the new version yet.
  def destApp   = "tasks-green"
  def activeApp = ""

  stage('A/B Production Deployment') {
      // Replace xyz-tasks-dev and xyz-tasks-prod with
      // your project names
      //activeApp = sh(returnStdout: true, script: "oc get route tasks -n xyz-tasks-prod -o jsonpath='{ .spec.to.name }'").trim()
      //if (activeApp == "tasks-green") {
        //destApp = "tasks-blue"
      //}
      echo "Active Application:      " + activeApp
      echo "Destination Application: " + destApp

      // Update the Image on the Production Deployment Config
      //sh "oc set image dc/${destApp} ${destApp}=docker-registry.default.svc:5000/xyz-tasks-dev/tasks:${prodTag} -n xyz-tasks-prod"

      // Update the Config Map which contains the users for the Tasks application
      //sh "oc delete configmap ${destApp}-config -n xyz-tasks-prod --ignore-not-found=true"
      //sh "oc create configmap ${destApp}-config --from-file=./configuration/application-users.properties --from-file=./configuration/application-roles.properties -n xyz-tasks-prod"

      // Deploy the inactive application.
      // Replace xyz-tasks-prod with the name of your production project
      //openshiftDeploy depCfg: destApp, namespace: 'xyz-tasks-prod', verbose: 'false', waitTime: '', waitUnit: 'sec'
      //openshiftVerifyDeployment depCfg: destApp, namespace: 'xyz-tasks-prod', replicaCount: '1', verbose: 'false', verifyReplicaCount: 'true', waitTime: '', waitUnit: 'sec'
      //openshiftVerifyService namespace: 'xyz-tasks-prod', svcName: destApp, verbose: 'false'
  }

  stage('Switch over to new Version') {
    input "Switch Production?"

    echo "Switching Production application to ${destApp}."
    // Replace xyz-tasks-prod with the name of your production project
   // sh 'oc patch route tasks -n xyz-tasks-prod -p \'{"spec":{"to":{"name":"' + destApp + '"}}}\''
  }

}

// Convenience Functions to read variables from the pom.xml
// Do not change anything below this line.
// --------------------------------------------------------
def getVersionFromPom(pom) {
  def matcher = readFile(pom) =~ '<version>(.+)</version>'
  matcher ? matcher[0][1] : null
}
