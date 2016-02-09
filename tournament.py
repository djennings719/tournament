#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#
from contextlib import contextmanager
import psycopg2


@contextmanager
def get_cursor():
    """
    Query helper function using context lib. Creates a cursor from a database
    connection object, and performs queries using that cursor.
    """
    db = connect()
    cursor = db.cursor()
    try:
        yield cursor
    except:
        raise
    else:
        db.commit()
    finally:
        cursor.close()
        db.close()


def connect():
    """
    Connect to the PostgreSQL database.
    Returns a database connection.
    """

    try:
        return psycopg2.connect("dbname=tournament")
    except:
        print "Was unable to connect to the database"


def delete_matches():
    """
    Remove all the match records from the database.
    """

    # put our delete statement in string form
    delete_matches_query = "delete from matches"

    # execute and commit our query, then close our cursor
    with get_cursor() as delete_matches_cursor:
        delete_matches_cursor.execute(delete_matches_query)


def delete_players():
    """
    Remove all the player records from the database.
    """
    # put our delete statement in string form
    # CASCADE our delete because if we have no players we should have no matches
    delete_players_query = "delete from players CASCADE"

    # execute and commit our query, then close our cursor
    with get_cursor() as delete_players_cursor:
        delete_players_cursor.execute(delete_players_query)


def count_players():
    """Returns the number of players currently registered."""
    # put our query in a string
    count_players_query = """select count(*) from players"""

    # execute our query
    # get all results
    # parse our information from the result set
    # close our cursor
    with get_cursor() as count_players_cursor:
        count_players_cursor.execute(count_players_query)
        fetchall = count_players_cursor.fetchall()
        count = fetchall[0][0]

    return count


def register_player(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    # our insert string
    register_player_query = """INSERT INTO players (name) values (%s);"""

    # execute our insert statement with the name parameter
    # commit the insert and close our cursor
    with get_cursor() as register_player_cursor:
        register_player_cursor.execute(register_player_query, (name,))


def player_standings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    # create a string to query our view
    player_standings_query = """select * from player_standings_view
                                order by wins desc;"""

    # execute our query
    # get all results
    with get_cursor() as player_standings_cursor:
        player_standings_cursor.execute(player_standings_query)
        standings = player_standings_cursor.fetchall()

    return standings


def report_match(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # create our query string
    # winner will be listed first and in the winner column
    # loser will be listed second
    report_match_query = """insert into matches (id1, id2, winner) values (%s, %s, %s) """

    # execute our query
    # commit our changes
    # close our cursor
    with get_cursor() as report_match_cursor:
        report_match_cursor.execute(report_match_query, (winner, loser, winner,))


def swiss_pairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    current_standings = player_standings()
    zipped_pairings = zip(current_standings)

    pairings = []

    for i in range(0, len(zipped_pairings), 2):
        pairings.append(zipped_pairings[i:i + 2])

    return_pairings = []
    for i in range(0, len(pairings), 1):
        return_pairings.append((pairings[i][0][0][0],
                                pairings[i][0][0][1],
                                pairings[i][1][0][0],
                                pairings[i][1][0][1],))

    return return_pairings
