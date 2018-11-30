#!groovy

// Run this pipeline on the custom Jenkins Slave ('jobtech-appdev')
// Jenkins Slaves have JDK and Maven already installed
// 'jobtech-appdev' has skopeo installed as well.
node('jobtech-appdev'){

  // The following variables need to be defined at the top level and not inside the scope of a stage - otherwise they would not be accessible from other stages.
  def version    = "1"
  //def chechoutDir = "/tmp/workspace/sokapi-pipeline"

  // Set the tag for the development image: version + build number
  def devTag  = "${version}-${BUILD_NUMBER}"

  // Set the tag for the production image: version
  def prodTag = "p-${devTag}"

  def branchName = env.BRANCH_NAME;
  def gitBranchName = env.GIT_BRANCH;
  def gitLocalbranchName = env.GIT_LOCAL_BRANCH;


  // Checkout Source Code
  stage('Checkout Source') {
  echo "Branch is: ${env.BRANCH_NAME}"
    checkout scm
    echo "Branch Name: ${branchName}"
    echo "GIT Branch Name: ${gitBranchName}"
    echo "Local GIT Branch Name: ${gitLocalbranchName}"
  }

  // Call SonarQube for Code Analysis
  stage('Code Analysis') {
    echo "Running Code Analysis"
    // requires SonarQube Scanner 2.8+
    def scannerHome = tool 'Jobtech_Sokapi_SonarScanner';
    echo "Scanner Home: ${scannerHome}"
    //sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=jobtech_sokapi -Dsonar.sources=. -Dsonar.host.url=http://sonarqube-jt-sonarqube.dev.services.jtech.se -Dsonar.login=${sonarqube_token}"
    withSonarQubeEnv('Jobtech_SonarQube_Server') {
      sh "${scannerHome}/bin/sonar-scanner -Dsonar.projectKey=jobtech_sokapi -Dsonar.sources=."
    }

    branchName = sh(returnStdout: true, script: "git show-branch")
    echo "Branch Name: ${branchName}"

  }

  // Build the OpenShift Image in OpenShift, tag and pus to nexus.
  stage('Build and Tag OpenShift Image') {
    echo "Building OpenShift container image sokapi:${devTag}"

    // Start Binary Build in OpenShift using the file we just published
    sh "oc start-build sokapi -n jt-dev --follow"

    //sh "oc new-app jt-dev/sokapi:${devTag} --name=sokapi --allow-missing-imagestream-tags=true -n jt-dev"
    //sh "oc set triggers dc/sokapi --remove-all -n jt-dev"

    // Tag the image using the devTag
    sh "oc tag jt-dev/sokapi:latest jt-dev/sokapi:${devTag} -n jt-dev"

    echo "Publish to Nexus sokapi_releases repository"
    //sh "${mvnCmd} deploy -DskipTests=true -DaltDeploymentRepository=nexus::default::http://nexus3-jt-nexus.dev.services.jtech.se/repository/sokapi_releases/"
  }

  // Deploy the built image to the Development Environment.
  stage('Deploy to Dev Env') {
    echo "Deploying container image to Development Env Project"

    echo "DEV TAGGING"
    sh "oc tag jt-dev/sokapi:latest jt-dev/sokapi:${devTag} -n jt-dev"

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

  // A/B Deployment into Production
  // -------------------------------------
  // Do not activate the new version yet.
  def destApp   = "sokapi-a"
  def activeApp = ""
  stage('A/B Production Deployment') {
    //if ( branchName != null && branchName.contains("prod") ){
        input "Deploy to Production?"
        activeApp = sh(returnStdout: true, script: "oc get route sokapi -n jt-prod -o jsonpath='{ .spec.to.name }'").trim()
        if (activeApp == "sokapi-a") {
          destApp = "sokapi-b"
        }
        echo "Active Application:      " + activeApp
        echo "Destination Application: " + destApp
        // Update the Image on the Production Deployment Config
        sh "oc set image dc/${destApp} ${destApp}=docker-registry.default.svc:5000/jt-dev/sokapi:${devTag} -n jt-prod"

        // Deploy the inactive application.
        openshiftDeploy depCfg: destApp, namespace: 'jt-prod', verbose: 'false', waitTime: '', waitUnit: 'sec'
        openshiftVerifyDeployment depCfg: destApp, namespace: 'jt-prod', replicaCount: '1', verbose: 'false', verifyReplicaCount: 'true', waitTime: '', waitUnit: 'sec'

        input "Switch Production?"
        echo "Switching Production application to ${destApp}"
        sh 'oc patch route sokapi -n jt-prod -p \'{"spec":{"to":{"name":"' + destApp + '"}}}\''
        //sh "oc set route-backends web ${destApp}=100 ${activeApp}=0"

      //}
    }
}
