from basescript import BaseScript

import sqlite3
import importlib

class ParserTester(BaseScript):
    DESC = 'Helps in iteratively developing string parsing functions'
    LOG_LEVEL = 'INFO'

    def define_args(self, parser):
        parser.add_argument('strings_file', metavar='strings-file', type=str,
            help='Text file containing one string per line')
        parser.add_argument('state_file', metavar='state-file', type=str,
            help='SQLite db file where parse cases are maintained')
        parser.add_argument('parser_class', metavar='parser-class', type=str,
            help='Import string for parser class')
        parser.add_argument('--parser-class-data-dir', type=str, default=None,
            help='Directory containing input data files for parser class to use')

    def ensure_table(self, db):
        # Ensures that required table(s) are present in db
        db.execute('''
            CREATE TABLE IF NOT EXISTS mappings (
                string text PRIMARY KEY,
                parsed text
            )''')

    def get_expected_mapping(self, db, x):
        # Get the parsed mapping for string @x from db if present
        # return None if no mapping is found
        db.execute('SELECT parsed FROM mappings WHERE string=?', (x,))
        rows = db.fetchall()
        return eval(rows[0][0]) if rows else None

    def store_expected_mapping(self, db, x, parsed):
        # Store the correct parsed version @parsed of string @x in db
        # If an entry is already present for @x, replace it
        parsed = repr(parsed)
        db.execute('''INSERT OR REPLACE INTO mappings (string, parsed)
            VALUES (?, ?)''', (x, parsed))

    def create_parser(self, parser_class, data_dir):
        module, klass = parser_class.rsplit('.', 1)
        m = importlib.import_module(module)
        k = getattr(m, klass)
        parser = k(data_dir)
        return parser

    def get_user_validation(self):
        x = raw_input("Is the parse correct? (Y/n): ")
        x = x.strip().lower()
        x = x or 'y'
        x = x[0]

        return x == 'y'

    def run(self):
        conn = sqlite3.connect(self.args.state_file)
        db = conn.cursor()

        self.ensure_table(db)
        conn.commit()

        parser = self.create_parser(self.args.parser_class,
            self.args.parser_class_data_dir)

        # counters

        n = 0  # Total cases examined
        n_passed_lookup = 0 # Passed because of expectation match from db
        n_passed_user = 0 # Passed because of user confirmation
        n_failed_lookup = 0 # Failed because of expectation mismatch from db
        n_failed_user = 0 # Failed because of user confirmation of failure
        n_exceptions = 0 # Failed due to unhandled exceptions

        for line in open(self.args.strings_file):
            x = line[:-1] # remove newline at end
            try:
                p = parser.parse(x)
            except SystemExit: raise
            except KeyboardInterrupt:
                break
            except:
                self.log.exception('During parsing of Line %d: "%s"' % (n+1, x))
                n_exceptions += 1
                continue

            n += 1
            self.log.info('PARSED: "%s" => %s' % (x, repr(p)))

            ep = self.get_expected_mapping(db, x)
            if ep:
                if p != ep: # expectation failed
                    n_failed_lookup += 1
                    self.log.info('FAIL: expected %s but got %s' % (repr(ep), repr(p)))
                else: # expectation passed
                    n_passed_lookup += 1

            else:
                # No previous expectation
                try:
                    correct = self.get_user_validation()
                except SystemExit: raise
                except KeyboardInterrupt:
                    break

                if correct:
                    # Store expectation
                    self.store_expected_mapping(db, x, p)
                    conn.commit()
                    n_passed_user += 1
                else:
                    n_failed_user += 1

        # print stats
        print
        L = locals()
        stats = dict((x, L[x]) for x in L.iterkeys() if x == 'n' or x.startswith('n_'))
        self.log.info(repr(stats))

def main():
    ParserTester().run()

if __name__ == '__main__':
    main()
