%token CONFIG_SYMBOL
%token ASSIGNMENT
%token V_HEXA
%token V_DECIMAL
%token V_STRING
%token V_YES
%token V_MODULE
%token E_INVALCHAR

%{

#include "../lib/lkc.h"
#include "../lib/config_symbol.h"

void yyerror(char *);
int yylex(void);

void print_cs_node(struct cs_node *);
void print_all_node();

struct cs_node *temp;
extern char *symbol_name; /* config symbol name */
extern char *text; /* string value */
%}

%%
program:
	program start
	|
	;

start:
	CONFIG_SYMBOL ass	{
		temp->name = symbol_name;
		insert_cs_node(temp);
		print_cs_node(temp);
		/* print_all_node(); */
	}
	| E_INVALCHAR {
		if (search_cs_node(symbol_name, temp) >= 0)
			print_all_node();
			/* print_cs_node(temp); */
		else
			printf("no declaration\n");
	}
	/*
	 * | CONFIG_SYMBOL {
	 *       if (search_cs_node(symbol_name, temp) >= 0)
	 *             print_cs_node(temp);
	 *       else
	 *             printf("no declaration\n");
	 * }
	 */
	;



ass:
	ASSIGNMENT val	

	/* CONFIG_SYMBOL ass */
	/*
	 * CONFIG_SYMBOL ass	{ 
	 *       temp->name = symbol_name;
	 *       insert_cs_node(temp);
	 *       print_cs_node(temp);
	 * }
	 * | CONFIG_SYMBOL	{
	 *       if (search_cs_node(symbol_name, temp) >= 0)
	 *             print_cs_node(temp);
	 *       else
	 *             printf("no declaration\n");
	 * }
	 */
	;

/*
 * ass:
 *       ASSIGNMENT val {
 *             temp->name = symbol_name;
 *             insert_cs_node(temp);
 *             print_cs_node(temp);
 *       }
 *       |
 *       {
 *             if (search_cs_node(symbol_name, temp) >= 0)
 *                   print_cs_node(temp);
 *             else
 *                   printf("no declaration\n");
 *       }
 *       ;
 */

val:
	V_STRING	{
		temp = (struct cs_node *)xmalloc(sizeof(struct cs_node));
		temp->data.str = text;
		temp->type = T_STRING;
	}
	| V_HEXA	{
		temp = (struct cs_node *)xmalloc(sizeof(struct cs_node));
		temp->data.ull = $1;
		temp->type = T_HEXA;
	}
	| V_DECIMAL {
		temp = (struct cs_node *)xmalloc(sizeof(struct cs_node));
		temp->data.ull = $1;
		temp->type = T_DECIMAL;
	}
	| V_MODULE	{ 
		temp = (struct cs_node *)xmalloc(sizeof(struct cs_node));
		temp->type = T_MODULE;
	}
	| V_YES	{ 
		temp = (struct cs_node *)xmalloc(sizeof(struct cs_node));
		temp->type = T_YES;
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

void print_all_node()
{
	int i;
	printf("nr_cs: %d\n", nr_cs);
	for (i = 0; i < nr_cs; i++) {
		printf("%d: ", i);
		print_cs_node(cs_table[i]);
	}
}

void print_cs_node(struct cs_node *node)
{
		switch (node->type) {
		case T_STRING:
			printf("%s = %s\n", node->name, node->data.str);
			break;
		case T_HEXA:
			printf("%s = 0x%llX\n", node->name, node->data.ull);
			break;
		case T_DECIMAL:
			printf("%s = %llu\n", node->name, node->data.ull);
			break;
		case T_YES:
			printf("%s = y\n", node->name);
			break;
		case T_MODULE:
			printf("%s = m\n", node->name);
			break;
		}
}
