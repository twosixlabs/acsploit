import argparse
import pprint


def get_orientation(origin, p1, p2):
    '''
    Returns the orientation of the Point p1 with regards to Point p2 using origin.
    Negative if p1 is clockwise of p2.
    :param origin:
    :param p1:
    :param p2:
    :return: integer
    '''
    difference = (
            ((p2[0] - origin[0]) * (p1[1] - origin[1]))
            - ((p1[0] - origin[0]) * (p2[1] - origin[1]))
    )

    return difference


def jarvis_march(points):
    hull = []
    candidates_checked = 0

    points = sorted(points, key=lambda x: x[0])  # sort by x-coordinate
    hull.append(points[0])  # first point is the left-most point

    last_point = points[0]
    new_point = None
    while new_point is not points[0]:
        # pick any point in the list that isn't the last point
        for p in points:
            if p is not last_point:
                new_point = p
                candidates_checked += 1
                break

        # check all points, snapping to any point that is left (ie outside) of the current new_point
        for p in points:
            if p is not last_point and p is not new_point:
                relative_direction = get_orientation(last_point, new_point, p)
                candidates_checked += 1
                if relative_direction > 0:
                    new_point = p

        hull.append(new_point)
        last_point = new_point

    return hull, candidates_checked


def parse_points(points_file):
    with open(points_file) as points_data:
        return [tuple([int(x) for x in line[1:-2].split(', ')]) for line in points_data.readlines()]


def main():
    parser = argparse.ArgumentParser(description='Implementation of the Jarvis March convex hull-finding algorithm to demonstrate ACsploit')
    parser.add_argument('points', help='File containing a list of non-colinear points in a plane')
    args = parser.parse_args()

    points = parse_points(args.points)
    hull, checks = jarvis_march(points)

    print('The convex hull is the points:')
    pprint.pprint(hull)
    print('Computing this convex hull required checking %i candidate points' % checks)


if __name__ == '__main__':
    main()
