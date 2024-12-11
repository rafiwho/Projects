#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

typedef struct STUDENT {
	char name[100];
	char id[100];
	char email[100];
	char cell[100];
	char blood[100];
	struct STUDENT *next;
} STUDENT;

STUDENT *insert(STUDENT *head, char name[], char id[], char email[], char cell[], char blood[]) {
	// creating new node for storing data
	STUDENT *temp_student = (STUDENT*)malloc(sizeof(STUDENT));
	strcpy(temp_student->name, name);
	strcpy(temp_student->id, id);
	strcpy(temp_student->email, email);
	strcpy(temp_student->cell, cell);
	strcpy(temp_student->blood, blood);

	if (head == NULL) {
		// if head is null that means this is the first node
		head = temp_student;
	} else {
		// if not empty inserting at the beginning of the head
		temp_student->next = head;
		head = temp_student;
	}
	return head;
};

void display(STUDENT *head) {
	STUDENT *temp_student = head;
	while (temp_student != NULL) {
		printf("\nName : %s\n", temp_student->name);
		printf("Id : %s\n", temp_student->id);
		printf("Email : %s\n", temp_student->email);
		printf("Cell : %s\n", temp_student->cell);
		printf("Blood group : %s\n", temp_student->blood);
		temp_student = temp_student->next;
	}
}

STUDENT *delete(STUDENT *head, char name[]) {
	STUDENT *temp1 = head;
	STUDENT *temp2 = head;
	while (temp1 != NULL) {
		if (!strcmp(temp1->name, name)) {
			if (temp1 == temp2) {
				// this means this is the first node
				head = head->next;
				free(temp1);
			}
			else {
				// we need to delete temp1 so we connect temp's pre node to temp's next node
				temp2->next = temp1->next;
				free(temp1);
			}
		}
		temp2 = temp1; // for storing precious node of expected deleting node
		temp1 = temp1->next;
	}
	return head;
}

void search_with_id(STUDENT *head, char id[]) {

	STUDENT *temp_student = head;

	while (temp_student != NULL) {

		// strcmp return 0 if found matches
		if (!strcmp(temp_student->id, id)) {
			printf("\nName : %s\n", temp_student->name);
			printf("Id : %s\n", temp_student->id);
			printf("Email : %s\n", temp_student->email);
			printf("Cell : %s\n", temp_student->cell);
			printf("Blood group : %s\n", temp_student->blood);
			return ;
		}
		temp_student = temp_student->next;
	}
	printf("Student's information not found\n");
}
void search_with_blood_group(STUDENT *head, char blood[]) {

	STUDENT *temp_student = head;

	while (temp_student != NULL) {

		// strcmp return 0 if found matches
		if (!strcmp(temp_student->blood, blood)) {
			printf("\nName : %s\n", temp_student->name);
			printf("Id : %s\n", temp_student->id);
			printf("Email : %s\n", temp_student->email);
			printf("Cell : %s\n", temp_student->cell);
			printf("Blood group : %s\n", temp_student->blood);
			return ;
		}
		temp_student = temp_student->next;
	}
	printf("Student's information not found\n");
}
void search_with_name(STUDENT *head, char name[]) {

	STUDENT *temp_student = head;

	while (temp_student != NULL) {

		// strcmp return 0 if found matches
		if (!strcmp(temp_student->name, name)) {
			printf("\nName : %s\n", temp_student->name);
			printf("Id : %s\n", temp_student->id);
			printf("Email : %s\n", temp_student->email);
			printf("Cell : %s\n", temp_student->cell);
			printf("Blood group : %s\n", temp_student->blood);
			return ;
		}
		temp_student = temp_student->next;
	}
	printf("Student's information not found\n");
}
void search_with_cell(STUDENT *head, char cell[]) {

	STUDENT *temp_student = head;

	while (temp_student != NULL) {

		// strcmp return 0 if found matches
		if (!strcmp(temp_student->cell, cell)) {
			printf("\nName : %s\n", temp_student->name);
			printf("Id : %s\n", temp_student->id);
			printf("Email : %s\n", temp_student->email);
			printf("Cell : %s\n", temp_student->cell);
			printf("Blood group : %s\n", temp_student->blood);
			return ;
		}
		temp_student = temp_student->next;
	}
	printf("Student's information not found\n");
}
void search_with_email(STUDENT *head, char email[]) {

	STUDENT *temp_student = head;

	while (temp_student != NULL) {

		// strcmp return 0 if found matches
		if (!strcmp(temp_student->email, email)) {
			printf("\nName : %s\n", temp_student->name);
			printf("Id : %s\n", temp_student->id);
			printf("Email : %s\n", temp_student->email);
			printf("Cell : %s\n", temp_student->cell);
			printf("Blood group : %s\n", temp_student->blood);
			return ;
		}
		temp_student = temp_student->next;
	}
	printf("Student's information not found\n");
}

int main() {
	STUDENT *head = NULL;
	char name[100];
	char id[100];
	char email[100];
	char cell[100];
	char blood[100];
	int choice = 1;
	while (choice) {
		printf("1 for inserting student's details :\n");
		printf("2 for all student's information :\n");
		printf("3 for deleting a student's details using name :\n");
		printf("4 for searching student's details with id :\n");
		printf("5 for searching student's details with blood group :\n");
		printf("6 for searching student's details with email :\n");
		printf("7 for searching student's details with cell :\n");
		printf("8 for searching student's details with name :\n");
		printf("Enter your choice :\n");
		scanf("%d", &choice);
		getchar();
		switch (choice) {
		case 1:
			printf("Enter student's name : ");

			fgets(name, 100, stdin);

			printf("Enter student's id : ");
			fgets(id, 100, stdin);

			printf("Enter student's email : ");
			fgets(email, 100, stdin);

			printf("Enter student's cell no : ");
			fgets(cell, 100, stdin);

			printf("Enter student's blood group : ");
			fgets(blood, 100, stdin);

			head = insert(head, name, id, email, cell, blood);
			break;
		case 2:
			display(head);
			break;
		case 3:
			printf("Enter a name for deletion : ");
			fgets(name, 100, stdin);
			head = delete(head, name);
			break;
		case 4:
			printf("Enter a id for searching : ");
			fgets(id, 100, stdin);
			search_with_id(head, id);
			break;
		case 5:
			printf("Enter a blood group for searching : ");
			fgets(blood, 100, stdin);
			search_with_blood_group(head, blood);
			break;
		case 6:
			printf("Enter an email for searching : ");
			fgets(email, 100, stdin);
			search_with_email(head, email);
			break;
		case 7:
			printf("Enter a cell number for searching : ");
			fgets(cell, 100, stdin);
			search_with_cell(head, cell);
			break;
		case 8:
			printf("Enter a name for searching : ");
			fgets(name, 100, stdin);
			search_with_name(head, name);
			break;
		default:
			if (choice)
				printf("Wrong input\n");
			break;
		}
	}
	int x = 6;
	while (--x) {
		sleep(1);
		printf("The program is exiting in %d second\n", x);
	}
	return 0;
}
