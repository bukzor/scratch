
def quote(argument):
 	return '"%s"' % (
        argument
        .replace('\\', r'\\')
        .replace(r'"', r'\"')
        .replace(r'$', r'\$')
        .replace(r'`', r'\`')
        .replace(r'!', r'\!')
    )

def main():
	from sys import argv
	print ' '.join(
		quote(quote(arg))
		for arg in argv[1:]
	)

if __name__ == '__main__':
	main()
