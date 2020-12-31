/*##############################################################################################################################
#
#  Author: Yan
#  Github: https://github.com/yan-wyb
#  Email : yan-wyb@foxmai.com
#
###############################################################################################################################*/


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <fcntl.h>
#include <dirent.h>
#include <linux/input.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/select.h>
#include <sys/time.h>
#include <termios.h>
#include <signal.h>


char convert[51] = {' ',' ', '1', '2', '3', '4','5','6','7','8','9',
				 '0',' ',' ',' ',' ','q','w','e','r','t',
				 'y','u','i','o','p',' ',' ',' ',' ','a',
				 's','d','f','g','h','j','k','l',':',' ',
				 ' ',' ',' ','z','x','c','v','b','n', 'm'};



void handler (int sig)
{
	printf ("nexiting...(%d)n", sig);
	exit (0);
}

void perror_exit (char *error)
{
	perror (error);
	handler (9);
}

int main (int argc, char *argv[])
{
	struct input_event buff;
	FILE *fp = NULL;
	int fd, rd,value, size = sizeof (struct input_event),i=0;
	char name[256] = "Unknown";
	char *device = NULL;
	char convert_value[17]={':',':',':',':',':',':',':',':',':',':',':',':',':',':',':',':',':'};
	char *value_pointer;

	if (argv[1] == NULL){
		printf("Please specify (on the command line) the path to the dev event interface devicen");
		exit (0);
	}

	if ((getuid ()) != 0)
		printf ("You are not root! This may not work...n");

	if (argc > 1)
		device = argv[1];

	if ((fd = open (device, O_RDONLY)) == -1)
		printf ("%s is not a vaild device.n", device);

	//Print Device Name
	ioctl (fd, EVIOCGNAME (sizeof (name)), name);
	printf ("Reading From : %s (%s)\n", device, name);

	while (1){
		while(read(fd,&buff,sizeof(struct input_event))==0);
		if (buff.value == 1 && buff.type == 1  && buff.code != 42){
			printf("i:%d,type:%d code:%d value:%d\n",i,buff.type,buff.code,buff.value); 
			printf("convert:%c\n",convert[buff.code]); 
			convert_value[i]=convert[buff.code];
			i++;
			if(i == 17){
				break;
			}
		}
	}
	printf("%s\n",convert_value);
	close(fd);
	fp = fopen("/tmp/eth_mac.txt", "w+");
	if(fp == NULL){
		printf("OPEN FILE ERROR\n");
	}
	size = sizeof(char);
	fwrite(convert_value, size, 17, fp);
	if(rd == EOF){
		printf("write eth_mac faile\n");
	}
	rewind(fp);
	fwrite(convert_value, size, 17, fp);
	if(rd == EOF){
    	printf("write eth_mac faile\n");
	}
	fclose(fp);
	return 0;
} 
