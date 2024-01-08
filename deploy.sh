#!/bin/bash


print_status() {
    echo -e "\e[32m$1\e[0m"
}


print_status "Sourcing config and secrets..."
source ./containerapp-config.env

required_vars=(
    "RESOURCE_GROUP"
    "VNET_RG"
    "VNET_NAME"
    "SUBNET_NAME"
    "ENVIRONMENT"
    "LOCATION"
    "FRONTEND_NAME"
    "FRONTEND_IMAGE"
    "FRONTEND_TARGET_PORT"
    "BACKEND_NAME"
    "BACKEND_IMAGE"
    "BACKEND_TARGET_PORT"
    "ACR_NAME" 
    "USE_SQLLITE"
    "SQL_SERVER_CONNECTION_STRING"
)


# Loop through the required variables and check if they are set
for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        read -rp "Please enter the value for $var: " "$var"
    fi
done




print_status "Checking if resource group $RESOURCE_GROUP exists..."
resource_group=$(az group show -n $RESOURCE_GROUP | jq -r '.id')

if [ -z "${resource_group}" ]
then
    print_status "\e[32m\nResource group $RESOURCE_GROUP not found. Creating...\n\e[0m"
    az group create -n $RESOURCE_GROUP -l $LOCATION
fi

print_status "Checking subnet $SUBNET_NAME"

INFRASTRUCTURE_SUBNET=$(az network vnet subnet show  --name $SUBNET_NAME --resource-group $VNET_RG --vnet-name $VNET_NAME | jq -r '.id')

if [ -z "${INFRASTRUCTURE_SUBNET}" ]
then
    print_status "\nSubnet $SUBNET_NAME not found. Exiting...\n"
    exit 1
fi

#check if containerapp environment exists
print_status "Checking if containerapp environment $ENVIRONMENT exists..."
containerapp_environment=$(az containerapp env show -n $ENVIRONMENT -g $RESOURCE_GROUP | jq -r '.id')

if [ -z "${containerapp_environment}" ]
then
    print_status "\e[32m\nContainer App Environment $ENVIRONMENT not found. Creating...\n\e[0m"
    az containerapp env create -n $ENVIRONMENT --location $LOCATION -g $RESOURCE_GROUP   --infrastructure-subnet-resource-id $INFRASTRUCTURE_SUBNET
fi

if [ $? -ne 0 ]
then
    printf "\nError configuring containerapp environment. Exiting...\n"
    exit 1
fi


containerAppDefaultDomain="https://$BACKEND_NAME.$(az containerapp env show -n $ENVIRONMENT -g $RESOURCE_GROUP | jq -r '.properties.defaultDomain')"

print_status "Deploying BACKEND Container App..."

# Define the environment variables as an array
config=(
    "USE_SQLLITE=$USE_SQLLITE"
    "SQL_SERVER_CONNECTION_STRING=$SQL_SERVER_CONNECTION_STRING"
)

#build backend image
print_status "Building $BACKEND_NAME image..."
cd autogen-copilot
docker build -t $BACKEND_NAME:1.0 -f Dockerfile .
docker tag $BACKEND_NAME:1.0 $BACKEND_IMAGE
docker push $BACKEND_IMAGE

print_status "Creating Container App..."
az containerapp create   \
--name $BACKEND_NAME   \
--resource-group $RESOURCE_GROUP   \
--environment $ENVIRONMENT   \
--image $BACKEND_IMAGE    \
--min-replicas 1 \
--max-replicas 1 \
--target-port $BACKEND_TARGET_PORT   \
--ingress 'external'   \
--registry-server $ACR_NAME.azurecr.io   \
--query properties.configuration.ingress \
--env-vars "${config[@]}" 


echo "Done! $BACKEND_NAME is deployed to $containerAppDefaultDomain"

cd ..


containerAppDefaultDomain_FrontEnd="https://$FRONTEND_NAME.$(az containerapp env show -n $ENVIRONMENT -g $RESOURCE_GROUP | jq -r '.properties.defaultDomain')"


print_status "Deploying FRONTEND Container App..."

#build frontend image
print_status "Building $FRONTEND_NAME image..."
cd chat-fluentui
cat << EOF > src/config.json
{
    "backendAPIHost" : "$containerAppDefaultDomain"    
}
EOF

npm install
npm run build
docker build -t $FRONTEND_NAME:1.0 -f Dockerfile .
docker tag $FRONTEND_NAME:1.0 $FRONTEND_IMAGE
docker push $FRONTEND_IMAGE

print_status "Creating Container App..."
az containerapp create   \
--name $FRONTEND_NAME   \
--resource-group $RESOURCE_GROUP   \
--environment $ENVIRONMENT   \
--image $FRONTEND_IMAGE    \
--min-replicas 1 \
--max-replicas 1 \
--target-port $FRONTEND_TARGET_PORT   \
--ingress 'external'   \
--registry-server $ACR_NAME.azurecr.io   \
--query properties.configuration.ingress \


echo "Done! $FRONTEND_NAME is deployed to $containerAppDefaultDomain_FrontEnd"