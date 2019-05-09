%token CONFIG_SYMBOL
%token ASSIGNMENT
%token V_HEXA
%token V_DECIMAL
%token V_STRING
%token V_YES
%token V_MODULE
%token E_INVALCHAR

%{

#include <stdbool.h>
#include "../lib/lkc.h"

void yyerror(char *);
int yylex(void);

enum types {
	T_YES,
	T_MODULE,
	T_STRING,
	T_HEXA,
	T_DECIMAL,
	T_COUNT
};

struct config_symbol_table {
	char *name;
	enum types type;
	union {
		unsigned long long int ull;
		char *str;
	} data;
};

struct config_symbol_table *temp;
extern char *symbol_name;
extern char *text;
%}

%%
program:
	 program start
	 |
	 ;

start:
	/* CONFIG_SYMBOL {  } */
	CONFIG_SYMBOL ass { 
		/* temp = $2; */
		/* temp->name = (char *)$1; */
		temp->name = symbol_name;
		switch (temp->type) {
		case T_STRING:
			/* printf("config = %s\n", temp->data.str); */
			printf("%s = %s\n", temp->name, temp->data.str);
			break;
		case T_HEXA:
			/* printf("config = 0x%llX\n", temp->data.ull); */
			printf("%s = 0x%llX\n", temp->name, temp->data.ull);
			break;
		case T_DECIMAL:
			/* printf("config = %llu\n", temp->data.ull); */
			printf("%s = %llu\n", temp->name, temp->data.ull);
			break;
		case T_YES:
			/* printf("config = y\n"); */
			printf("%s = y\n", temp->name);
			break;
		case T_MODULE:
			/* printf("config = m\n"); */
			printf("%s = m\n", temp->name);
			break;
		}
	}
	/* { printf("config = %llu\n", $2); }*/
	;

ass:
	ASSIGNMENT val 
	/* ASSIGNMENT val { $$ = $2; } */
	;

val:
	V_STRING	{
				temp = (struct config_symbol_table *)xmalloc(sizeof(struct config_symbol_table));
				/* temp->data.str = (char *)$1; */
				temp->data.str = text;
				temp->type = T_STRING;
				/* $$ = temp; */
			}
	/* | V_HEXA { printf("heax\n"); } */
	| V_HEXA	{
				temp = (struct config_symbol_table *)xmalloc(sizeof(struct config_symbol_table));
				temp->data.ull = $1;
				temp->type = T_HEXA;
				/* $$ = temp; */
			}
	/* | V_DECIMAL { printf("decimal\n"); } */
	| V_DECIMAL {
				temp = (struct config_symbol_table *)xmalloc(sizeof(struct config_symbol_table));
				temp->data.ull = $1;
				temp->type = T_DECIMAL;
				/* $$ = temp; */
			}
	| V_MODULE	{ 
				temp = (struct config_symbol_table *)xmalloc(sizeof(struct config_symbol_table));
				temp->type = T_MODULE;
				/* $$ = temp; */
			}
	| V_YES	{ 
				temp = (struct config_symbol_table *)xmalloc(sizeof(struct config_symbol_table));
				temp->type = T_YES;
				/* $$ = temp; */
			}
	;

%%
void yyerror(char *s)
{
  printf("%s\n", s);
  return 0;
}

int main(void)
{
  yyparse();
  return 0;
}

