/**
 * @file phylib.h
 * @author Hisham Issa (hissa01@uoguelph.ca | 1194466)
 * @brief  Header file containing the typedef's, structure defintions and function prototypes
 * @date 2024-01-29
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define PHYLIB_BALL_RADIUS      (28.5) //mm
#define PHYLIB_BALL_DIAMETER    (2*PHYLIB_BALL_RADIUS)

#define PHYLIB_HOLE_RADIUS      (2*PHYLIB_BALL_DIAMETER)
#define PHYLIB_TABLE_LENGTH     (2700.0) //mm (long sides of the pool table)
#define PHYLIB_TABLE_WIDTH      (PHYLIB_TABLE_LENGTH/2.0) //mm (shorter ends of the table)

#define PHYLIB_SIM_RATE         (0.0001) //s
#define PHYLIB_VEL_EPSILON      (0.01) //mm/s

#define PHYLIB_DRAG             (150.0) //mm/s^2
#define PHYLIB_MAX_TIME         (600) //s

#define PHYLIB_MAX_OBJECTS      (26) //15 numbered balls, 1 cue ball, 6 holes, 4 cushions

typedef enum {
    PHYLIB_STILL_BALL   =0,
    PHYLIB_ROLLING_BALL =1,
    PHYLIB_HOLE         =2,
    PHYLIB_HCUSHION     =3,
    PHYLIB_VCUSHION     =4,
} phylib_obj;

// "phylib_coord" is now a data type to represent the coordinates of a ball (x, y)
typedef struct {
    double x;
    double y;
} phylib_coord;

//"phylib_still_ball" is the type for a still ball. Since it is not moving it only requires a position and a number (on the ball)
typedef struct {
    unsigned char number;
    phylib_coord pos;
} phylib_still_ball;

//"phylib_rolling_ball" is the type for a moving ball, so it needs a velocity and acceleration
typedef struct {
    unsigned char number;
    phylib_coord pos;
    phylib_coord vel;
    phylib_coord acc; //negative acceleration due to friction
} phylib_rolling_ball;

//"phylib_hole" simply is the holes on the table, so they only need a position
typedef struct {
    phylib_coord pos;
} phylib_hole;

//"hcushion" meaning horizontal cushions so they are only located on the y-axis's of the table
typedef struct {
    double y;
} phylib_hcushion;

//"vcushion" meaning vertical cushions so they are only located on the x-axis's of the table
typedef struct {
    double x;
} phylib_vcushion;

typedef union {
    phylib_still_ball still_ball;
    phylib_rolling_ball rolling_ball;
    phylib_hole hole;
    phylib_hcushion hcushion;
    phylib_vcushion vcushion;
} phylib_untyped;

typedef struct {
    phylib_obj type;
    phylib_untyped obj;
} phylib_object;

typedef struct {
    double time;
    phylib_object *object[PHYLIB_MAX_OBJECTS];
} phylib_table;

//Function prototypes for constructor methods

phylib_object *phylib_new_still_ball(unsigned char number, phylib_coord *pos);

phylib_object *phylib_new_rolling_ball(unsigned char number, phylib_coord *pos, 
                                        phylib_coord *vel, phylib_coord *acc  );

phylib_object *phylib_new_hole(phylib_coord *pos);

phylib_object *phylib_new_hcushion(double y);

phylib_object *phylib_new_vcushion(double x);

phylib_table *phylib_new_table(void);

//PART 2: Utility Functions

void phylib_copy_object(phylib_object **dest, phylib_object **src);

phylib_table *phylib_copy_table(phylib_table *table);

void phylib_add_object(phylib_table *table, phylib_object *object);

void phylib_free_table(phylib_table *table);

phylib_coord phylib_sub(phylib_coord c1, phylib_coord c2);

double phylib_length(phylib_coord c);

double phylib_dot_product(phylib_coord a, phylib_coord b);

double phylib_distance(phylib_object *obj1, phylib_object *obj2);

//PART 3: Movement

void phylib_roll(phylib_object *new, phylib_object *old, double time);

unsigned char phylib_stopped(phylib_object *object);

void phylib_bounce(phylib_object **a, phylib_object **b);

unsigned char phylib_rolling(phylib_table *t);

phylib_table *phylib_segment(phylib_table *table);

//NEW FUNCTION FOR A2 

char *phylib_object_string( phylib_object *object );
