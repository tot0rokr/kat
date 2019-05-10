%{
#include <string.h>
#include <stdlib.h>
void yyerror(char *);
#include "parser.tab.h"
#include "../lib/lkc.h"

char *symbol_name;
char *text;
%}

%%


#.*\n				/* Comment */
[ \t]			;	/* Space */

^CONFIG_[^#\n= \t]+	{	/* config symbol */
				symbol_name = (char *)xmalloc(strlen(yytext) + 1);		
				strncpy(symbol_name, yytext, strlen(yytext));
				return CONFIG_SYMBOL;
			}

={1}			return ASSIGNMENT;	/* Assignment */
y{1}			return V_YES;
m{1}			return V_MODULE;
\"[^#\n]*\"		{	/* Value String */
				text = (char *)xmalloc(strlen(yytext) + 1);
				strncpy(text, yytext, strlen(yytext));
				return V_STRING;
			}
0x[0-9A-Fa-f]+	{	/* Value Hexa Decimal */
				yylval = strtoull(yytext, NULL, 16);
				return V_HEXA;
			}
[0-9]+		{	/* Value Decimal */
				yylval = atoll(yytext);
				return V_DECIMAL;
			}


.			{
				yyerror("invalid character");
				return E_INVALCHAR;
			}
%%

int yywrap(void)
{
  return 1;
}


