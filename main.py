from sys import stderr

import program

@program.register_program
class gaussian(program.program):
    def __init__(self, args=None):
        argslist = [
			('--matrix', {
					'dest':		'matrix',
					'default':	False,
					'action':	'store',
					'type':		str
				}),
			('--out', {
					'dest':		'out',
					'default':	False,
					'action':	'store',
					'type':		str
			}),
			('--error-rate', {
					'dest':		'error_rate',
					'default':	0.01,
					'action':	'store',
					'type':		float
			}),
			('--injection-rate', {
					'dest':		'injection_rate',
					'default':  0.10,
					'action':	'store',
					'type':		float
			}),
			]
        super().__init__(argslist, args, desc="inject gaussian noise into a matrix")

    def run(self):
        args = self.arguments
        import gaussian
        g = gaussian.gaussian(args.matrix, args.out, args.error_rate,
                              args.injection_rate)
        g.run()


if __name__ == "__main__":
	print('[E] run materror instead', file=stderr)
