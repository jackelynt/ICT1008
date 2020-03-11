#include <stdio.h>
#include <string.h>
#include <malloc.h>
#include <stdbool.h>
#include <math.h>

int main()
{
    int diskSize = 256;
    printf("Enter number of block: ");
    int sizeOfBlock = 0;
    scanf("%d", &sizeOfBlock);
    printf("%d\n", sizeOfBlock);
    fflush(stdin);
    int noOfBlock = 256/sizeOfBlock;
    bool checkOfValidBlockSize = false;
    for (int i = 0; i < 8; i++)
    {
        if(noOfBlock == pow(2, i)){
            checkOfValidBlockSize = true;
        }
    }
    
    int* file_storage = malloc(256 * sizeof(int));
    int* file_ID = malloc(noOfBlock * sizeof(int));
    for (int i = 0; i < 256; i++)
    {
        file_storage[i] = 0;
        if(i < noOfBlock){
            file_ID[i] = 0;
        }
    }
    printf("File ID: \n");
    for (int i = 0; i < noOfBlock; i++)
    {
        printf("%d\t",file_ID[i]);
        if(i%10 == 0){
            printf("\n");
        }
    }
    
    printf("\nFile Storage: \n");
    for (int i = 0; i < 256; i++)
    {
        printf("%d\t",file_storage[i]);
        if(i%10 == 0){
            printf("\n");
        }
    }

    char user_input[20];
    printf("\nFile to be added or delete: ");
    fgets(user_input, 20, stdin);
    printf("%s\n", user_input);
    fflush(stdin);
    while (strcmp(user_input,"-1") != 0)
    {
        // Extract the first token
        char * token = strtok(user_input, " ");
        char *processString[4];
        int processCounter = 0;
        // loop through the string to extract all other tokens
        while( token != NULL ) {
        printf( "%s\n", token ); //printing each token
        processString[processCounter] = token;
        printf( "process: %s\n", processString[processCounter] ); //printing each token
        token = strtok(NULL, " ");
        processCounter++;
        }
        if(processString[0][0] ==  'a'){
            printf("\nAdd Process: \n");
            bool checkduplication = false;
            int tmp_ID = atoi(processString[1]);
            int noBlockAvailable = 0;
            for (int i = 0; i < (noOfBlock); i++){
                if(file_ID[i] == tmp_ID){
                    checkduplication = true;
                }
                if(file_ID[i] == 0){
                    noBlockAvailable++;
                }
            }
            if (checkduplication == true){
                printf("FileID used\n");
                break;
            }
            else{
                int tmp_noOfBlock = atoi(processString[2]);
                
                int counter = tmp_ID;
                if(noBlockAvailable >= tmp_noOfBlock){
                    for (int i = 0; i < noOfBlock; i++)
                    {
                        if(file_ID[i] == 0 && tmp_noOfBlock > 0){
                            file_ID[i] = tmp_ID;
                            tmp_noOfBlock--;
                            for (int j = 0; j < sizeOfBlock; j++)
                            {
                                counter++;
                                file_storage[sizeOfBlock*i+j] = counter;
                                printf("%d", sizeOfBlock*i+j);
                            }
                        }
                    }
                }
                else{
                    printf("Disk is full. End of program.");
                    break;
                }
            }
            //print to check
            printf("File ID: \n");
            for (int i = 0; i < noOfBlock; i++)
            {
                printf("%d\t",file_ID[i]);
                if(i%10 == 0){
                    printf("\n");
                }
            }
            printf("\nFile Storage: \n");
            for (int i = 0; i < 256; i++)
            {
                printf("%d\t",file_storage[i]);
                if(i%10 == 0){
                    printf("\n");
                }
            }
        }
         if(processString[0][0] == 'd'){
            printf("\nDelete Process: \n");
            int tmp_ID = atoi(processString[1]);
            
            for (int i = 0; i < noOfBlock; i++)
            {
                if (file_ID[i] == tmp_ID)
                {
                    file_ID[i] = 0;
                    for (int j = 0; j < sizeOfBlock; j++)
                    {
                        file_storage[sizeOfBlock*i+j] = 0;
                    }
                }
            }
            //print to check
            printf("File ID: \n");
            for (int i = 0; i < noOfBlock; i++)
            {
                printf("%d\t",file_ID[i]);
                if(i%10 == 0){
                    printf("\n");
                }
            }
            printf("\nFile Storage: \n");
            for (int i = 0; i < 256; i++)
            {
                printf("%d\t",file_storage[i]);
                if(i%10 == 0){
                    printf("\n");
                }
            }
        }

        printf("\nFile to be added or delete: ");
        gets(user_input);
        printf("%s\n", user_input);
        if(strcmp(user_input,"-1") == 0){
            break;
        }
    }
    
   
    return 0;
}
