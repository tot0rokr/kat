#include "./config_symbol.h"
#include "./lkc.h"
#include <string.h>
#include <stdlib.h>

void init_cs_table(void)
{
}

int insert_cs_node(struct cs_node *new)
{
	int i;
	int cmp_val;
	/* init table */
	if (!cs_table) {
		cs_table = (struct cs_node **)xmalloc(sizeof(struct cs_node *));
		nr_cs = 1;
		cs_table[0] = new;
		return 0;
	}

	/* update node */
	if ((i = search_cs_node(new->name, NULL)) >= 0) {
		free(cs_table[i]);
		cs_table[i] = new;
		return 0;
	}
	printf("i = %d\n", i);

	/* resize table for add node */
	cs_table = (struct cs_node **)xrealloc(cs_table,
		sizeof(struct cs_node *) * (nr_cs + 1));

	/* maintain sorted state and insert "new" */
	for (i = nr_cs - 1; i >= 0; i--) {
		cmp_val = strcmp(new->name, cs_table[i]->name);
		if (cmp_val < 0) {
			cs_table[i + 1] = cs_table[i];
		} else {
			break;
		}
	}
	cs_table[i + 1] = new;
	nr_cs += 1;
	return 0;
}


int search_cs_node(char *name, struct cs_node *res)
{
	int left = 0, right = nr_cs;
	int cur_i = (right - left) / 2;
	struct cs_node *cur = cs_table[cur_i];
	struct cs_node *temp;
	int cmp_val;

	if (!cs_table)
		return -ENOINI;
	/* binary search */
	do {
		cmp_val = strcmp(name, cur->name);
		if (cmp_val == 0) {
			res = cur;
			return cur_i;
		} else if(cmp_val < 0) {
			temp = cur;
			right = cur_i;
		} else {
			temp = cur;
			left = cur_i;
		}
		cur_i = left + (right - left) / 2;
		cur = cs_table[cur_i];
	} while (cur != temp);
	return -EEXCLU;
}
