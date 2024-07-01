/**
 * @file phylib.c
 * @author Hisham Issa (hissa01@uoguelph.ca)
 * @brief C Library that implements a number of functions to simulate the collision of billiard balls
 *        with cushions and other balls. 
 * @date 2024-01-29
 */

#include "phylib.h"

// PART 1: C Library for objects within the billiard simulation

/**
 * @brief Allocates memory for a new phylib_object, set it's type to PHYLIB_STILL_BALL
 * and transfer the information from the parameters to structure.
 * @param number @param pos 
 * @return phylib_object* 
 */
phylib_object *phylib_new_still_ball(unsigned char number, phylib_coord *pos) {
    phylib_object *newStillBall = (phylib_object *)malloc(sizeof(phylib_object));
    //Check if the memory allocation was successful. If not return NULL.
    if (newStillBall == NULL) {
        return NULL;
    }
    newStillBall->type = PHYLIB_STILL_BALL; //Set the type to PHYLIB_STILL_BALL

    //Transfer the information provided in the function parameters into the structure
    newStillBall->obj.still_ball.number = number;
    newStillBall->obj.still_ball.pos = *pos;

    return newStillBall; //Return a pointer to the new still ball
}

/**
 * @brief Allocates memory for a new phylib_object, set it's type to PHYLIB_ROLLING_BALL
 * and transfer the information from the parameters to structure.
 * @param number @param pos @param vel @param acc 
 * @return phylib_object* 
 */
phylib_object *phylib_new_rolling_ball(unsigned char number, phylib_coord *pos, phylib_coord *vel, phylib_coord *acc) {
    phylib_object *newRollingBall = (phylib_object *)malloc(sizeof(phylib_object));
    //Check if the memory allocation was successful. If not return NULL.
    if(newRollingBall == NULL) {
        return NULL;
    }
    newRollingBall->type = PHYLIB_ROLLING_BALL; //Set type to PHYLIB_ROLLING_BALL

    //Transfer the information provided in the function parameters into the structure
    newRollingBall->obj.rolling_ball.number = number;
    newRollingBall->obj.rolling_ball.pos = *pos;
    newRollingBall->obj.rolling_ball.vel = *vel;
    newRollingBall->obj.rolling_ball.acc = *acc;

    return newRollingBall; //Return pointer to the new rolling ball
}

/**
 * @brief Allocates memory for a new phylib_object, set it's type to PHYLIB_HOLE
 * and transfer the information from the parameters to structure.
 * @param pos 
 * @return phylib_object* 
 */
phylib_object *phylib_new_hole(phylib_coord *pos) {
    phylib_object *newHole = (phylib_object *)malloc(sizeof(phylib_object));
    //Check if the memory allocation was successful. If not return NULL
    if(newHole == NULL) {
        return NULL;
    }
    newHole->type = PHYLIB_HOLE; //Set type to PHYLIB_HOLE

    newHole->obj.hole.pos = *pos; //Transfer the information from parameters into the structure

    return newHole; //Return pointer to the new hole
}

/**
 * @brief Allocates memory for a new phylib_object, set it's type to PHYLIB_HCUSHION
 * and transfer the information from the parameters to structure.
 * @param y 
 * @return phylib_object* 
 */
phylib_object *phylib_new_hcushion(double y) {
    phylib_object *newHorizontalCushion = (phylib_object *)malloc(sizeof(phylib_object));
    //Check if memory allocation is successful. If not return NULL
    if (newHorizontalCushion == NULL) {
        return NULL;
    }
    newHorizontalCushion->type = PHYLIB_HCUSHION; //Set type to PHYLIB_HCUSHION

    newHorizontalCushion->obj.hcushion.y = y; //Transfer parameters into the structure

    return newHorizontalCushion; //Return pointer to new horizontal cushion
}

/**
 * @brief Allocates memory for a new phylib_object, set it's type to PHYLIB_VCUSHION
 * and transfer the information from the parameters to structure
 * @param x 
 * @return phylib_object* 
 */
phylib_object *phylib_new_vcushion(double x) {
    phylib_object *newVerticalCushion = (phylib_object *)malloc(sizeof(phylib_object));
    //Check if memory allocation is successful. If not return NULL.
    if (newVerticalCushion == NULL) {
        return NULL;
    }
    newVerticalCushion->type = PHYLIB_VCUSHION; //Set type to PHYLIB_VCUSHION

    newVerticalCushion->obj.vcushion.x = x; //Transfer parameters to structure

    return newVerticalCushion; //Return pointer to new vertical cushion
}

/**
 * @brief Allocates memory for a table structure. Then assigns the values of it's array elements to 
 * pointers to new objects created by the prior functions (phylib_new_*). Remaining pointers are set to NULL.
 * @return phylib_table* 
 */
phylib_table *phylib_new_table( void ) {
    phylib_table *newTable = (phylib_table *)malloc(sizeof(phylib_table));
    //Check if memory allocation is successful. If not return NULL
    if (newTable == NULL) {
        return NULL;
    }
    newTable->time = 0.0; //Set time to 0.0

    newTable->object[0] = phylib_new_hcushion(0.0); //New horizontal cushion at y = 0.0
    newTable->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH); //New horizontal cushion at PHYLIB_TABLE_LENGTH
    newTable->object[2] = phylib_new_vcushion(0.0); //New vertical cushion at x = 0.0
    newTable->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH); //New vertical cushion at x = PHYLIB_TABLE_WIDTH
    newTable->object[4] = phylib_new_hole(&(phylib_coord){0.0, 0.0}); //Hole in the bottom left corner
    newTable->object[5] = phylib_new_hole(&(phylib_coord){0.0, PHYLIB_TABLE_WIDTH}); //Hole in the top left corner
    newTable->object[6] = phylib_new_hole(&(phylib_coord){0.0, PHYLIB_TABLE_LENGTH}); //Hole in the bottom right corner
    newTable->object[7] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, 0.0}); //Hole in the top right corner
    newTable->object[8] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_LENGTH / 2.0, PHYLIB_TABLE_LENGTH / 2.0}); //Hole halfway up the table on the left
    newTable->object[9] = phylib_new_hole(&(phylib_coord){PHYLIB_TABLE_WIDTH, PHYLIB_TABLE_LENGTH}); //Hole halfway up the table on the right
    
    for (int i = 10; i < PHYLIB_MAX_OBJECTS; i++) {
            newTable->object[i] = NULL; //Set remaining pointers to NULL
    }

    return newTable; //Return the pointer to the new table
}

//PART 2: Utility Functions

/**
 * @brief Allocates new memory for a phylib_object. Saves the address of that object at the location
 * pointed to by @param dest, copy the contents of the objects from location of @param src. 
 * @param dest @param src 
 */
void phylib_copy_object(phylib_object **dest, phylib_object **src) {
    //Check if the memory location pointed to by src is NULL. If so set dest to NULL
    if (src == NULL || *src == NULL) {
        *dest = NULL;
    } else {
        //Allocate the memory for the new object
        phylib_object *newObject = (phylib_object *)malloc(sizeof(phylib_object));
        //Check if memory allocation was successful. If not return.
        if (newObject == NULL) {
            return;
        }
        memcpy(newObject, *src, sizeof(phylib_object)); //Copy the contents of src into newObject

        *dest = newObject; //Update the destination pointer to point to the newly allocated memory
    } 
}

/**
 * @brief Allocates memory for a new phylib_table. Content pointed to by table are copied to the
 * new memory location and returns the address.
 * @param table 
 * @return phylib_table* 
 */
phylib_table *phylib_copy_table(phylib_table *table) {
    //Check if table passed to the function is NULL. If so return NULL.
    if (table == NULL) {
        return NULL;
    }

    //Allocate memory for a new phylib_table called newTable
    phylib_table *newTable = (phylib_table *)malloc(sizeof(phylib_table));
    //Check if memory allocation was successful. If not return NULL
    if (newTable == NULL) {
        return NULL;
    }

    newTable->time = table->time; //Copy time from original table to newTable
    //Iterate over each object in the original table and copy them over
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; ++i) {
        if (table->object[i] != NULL) {
            //Allocate memory for each non-NULL object in the original table
            newTable->object[i] = (phylib_object *)malloc(sizeof(phylib_object));
            if (newTable->object[i] == NULL) {
                //If allocation for the object fails, free the memory and return NULL
                for (int j = 0; j < PHYLIB_MAX_OBJECTS; ++j) {
                    free(newTable->object[j]);
                }
                free(newTable);
                return NULL;
            }
            *newTable->object[i] = *table->object[i]; //Copy the contents of the original object to the new object

        } else {
            newTable->object[i] = NULL; //Set corresponding object in newTable to NULL if original is NULL
        }
    }

    return newTable; //Return a pointer to the newly created table
}

/**
 * @brief Iterates over the object array in table until it reaches a NULL pointer. Then assigns that
 * pointer to be equal to the address of object. If no NULL pointers are found, do nothing.
 * @param table @param object 
 */
void phylib_add_object(phylib_table *table, phylib_object *object) {
     //Check if table or object passed is NULL. If so return NULL.
    if (table == NULL || object == NULL) {
        return;
    }

    //Iterate over the array of objects in the table until a NULL pointer is found
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; ++i) {
        if (table->object[i] == NULL) {
            table->object[i] = object; //Assign the passed object to the NULL object
            return; //Exit the function
        }
    }
    //If no NULL pointer is ever reached do nothing. Exit function.
}

/**
 * @brief Free's every non-NULL pointer in the object array of table. Then free's table.
 * @param table 
 */
void phylib_free_table(phylib_table *table) {
    //Check if table is NULL. If so there is nothing to free, so return.
    if (table == NULL) {
        return;
    }

    //Iterate over the array of objects in the table until a non-NULL pointer is found
    for(int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if (table->object[i] != NULL) {
            free(table->object[i]); //Free the memory pointed to by the object pointer
            table->object[i] = NULL; //Set the object pointer to NULL
        }
    }
    free(table); //Free the table
}

/**
 * @brief Returns the difference of c1 and c2 for both x and y.    
 * @param c1 @param c2 
 * @return phylib_coord 
 */
phylib_coord phylib_sub(phylib_coord c1, phylib_coord c2) {
    phylib_coord difference;

    difference.x = c1.x - c2.x; //Difference between x values
    difference.y = c1.y - c2.y; //Difference between y values

    return difference;
}

/**
 * @brief Returns the length of the coordinate c by using the Pythagorean theorem. 
 * @param c 
 * @return double 
 */
double phylib_length(phylib_coord c) {
    double x_squared, y_squared, length;

    x_squared = c.x * c.x; // x * x = x^2
    y_squared = c.y * c.y; // y * y = y^2

    length = sqrt(x_squared + y_squared); //Square root of x^2 + y^2

    return length; // Return the length
}

/**
 * @brief Computes the dot-product between 2 coordinates. This is the sum of the product of 
 * x-values and y-values
 * @param a @param b 
 * @return double 
 */
double phylib_dot_product(phylib_coord a, phylib_coord b) {
    return (a.x * b.x) + (a.y * b.y); //Return the sum of the x and y value products
}

/**
 * @brief Calculates the distance between 2 objects. obj1 MUST be a PHYLIB_ROLLING_BALL, if not return -1.0.
 * Otherwise the distance between objects is calculates following rules outlined in A1.
 * @param obj1 @param obj2 
 * @return double 
 */
double phylib_distance(phylib_object *obj1, phylib_object *obj2) {
    //Check if either objects are NULL OR if obj1 is NOT a rolling ball. If so return -1.0
    if (obj1 == NULL || obj2 == NULL || obj1->type != PHYLIB_ROLLING_BALL) {
        return -1.0;
    }

    double distance;
    phylib_coord position; 
    position = obj1->obj.rolling_ball.pos;

    //Switch case handles the collision physics based on the type of the 2nd object (obj2).
    switch(obj2->type) {
        case PHYLIB_ROLLING_BALL:
            //Calculate the distance between the centers of the balls and subtract 2 ball radius's (diameter)
            distance = phylib_length(phylib_sub(position, obj2->obj.rolling_ball.pos)) - PHYLIB_BALL_DIAMETER;
            break;
        case PHYLIB_STILL_BALL:
            //Calculate the distance between the centers of the balls and subtract 2 ball radius's (diameter)
            distance = phylib_length(phylib_sub(position, obj2->obj.still_ball.pos)) - PHYLIB_BALL_DIAMETER;
            break;
        case PHYLIB_HOLE:
            //Calculate the distance to hole center and subtract hole radius
            distance = phylib_length(phylib_sub(position, obj2->obj.hole.pos)) - PHYLIB_HOLE_RADIUS;
            break;
        case PHYLIB_HCUSHION:
            //Calculate the distance between the center of the ball and the horizontal cushion and subtract ball radius
            distance = fabs(position.y - obj2->obj.hcushion.y) - PHYLIB_BALL_RADIUS;
            break;
        case PHYLIB_VCUSHION:
            //Calculate the distance between the center of the ball and the vertical cushion and subtract ball radius
            distance = fabs(position.x - obj2->obj.vcushion.x) - PHYLIB_BALL_RADIUS;
            break;
        default:
        //In this case, object 2 is not a valid type, exit (return -1.0 as stated in description)
        return -1.0;
    }

    return distance; //Return the distance
}

// PART 3: Functions to simulate the balls movement on the table

/**
 * @brief Updates a 'new' phylib_object that represents the 'old' phylib_object after it was rolled for a 
 * period of 'time'. Updates the values in 'new' according to the equations for position and velocity. 
 * If either velocities change sign (change direction) during the time interval then the velocity and corresponding 
 * acceleration are set to 0.
 * @param new @param old @param time 
 */
void phylib_roll(phylib_object *new, phylib_object *old, double time) {
    //Check if new or old point to a NULL location OR if old or new are NOT rolling balls. If so return.
    if (new == NULL || old == NULL || old->type != PHYLIB_ROLLING_BALL || new->type != PHYLIB_ROLLING_BALL) {
        return;
    }

    //Calculate the velocity of the new ball using formula: v = u + at
    phylib_coord new_vel;
    new_vel.x = old->obj.rolling_ball.vel.x + (old->obj.rolling_ball.acc.x * time);
    new_vel.y = old->obj.rolling_ball.vel.y + (old->obj.rolling_ball.acc.y * time);

    //Check for change in direction in the x-axis (sign change)
    if (old->obj.rolling_ball.acc.x != 0) {
        /* Calculate the time it takes for the ball's velocity in the x-direction to become 0. 
           Formula is derived from: v = u + at. 
           v is zero (since it is time to stop)
           u is initial velocity (old->obj.rolling_ball.vel.x)
           a is acceleration (old->obj.rolling_ball.acc.x). 
                a is multiplied by -1 (negative) to handle the deceleration. Time to stop is velocity 
                and acceleration in opposite directions (deceleration) 
           Rearranging the equation gives t = u / a which equals time to reach zero velocity */
        double time_to_zero_x = old->obj.rolling_ball.vel.x / (-1 * old->obj.rolling_ball.acc.x);
        //Check if time to zero falls within 0 and 'time'
        if(time_to_zero_x >= 0 && time_to_zero_x <= time) {
            //If velocity changes sign, set velocity and acceleration to 0
            new_vel.x = 0;
            old->obj.rolling_ball.acc.x = 0;
        }
    }
    //Check for change in direction in the y-axis (sign change)
    if (old->obj.rolling_ball.acc.y != 0) {
        //Calculate the time it takes for velocity in the y-direction to become 0 (same as x). 
        double time_to_zero_y = old->obj.rolling_ball.vel.y / (-1 * old->obj.rolling_ball.acc.y);
        //Check if time to zero falls within 0 and 'time'
        if (time_to_zero_y >= 0 && time_to_zero_y <= time) {
            //If velocity changes sign, set velocity and acceleration to 0
            new_vel.y = 0;
            old->obj.rolling_ball.acc.y = 0;
        }
    }

    new->obj.rolling_ball.vel = new_vel; //Assign the calculated velocity to the 'new' updated ball

    // Update the position (x and y) of the new ball using the equation of motion: s = ut + 0.5at^2
    new->obj.rolling_ball.pos.x = old->obj.rolling_ball.pos.x + old->obj.rolling_ball.vel.x * time + 0.5 * old->obj.rolling_ball.acc.x * time * time;
    new->obj.rolling_ball.pos.y = old->obj.rolling_ball.pos.y + old->obj.rolling_ball.vel.y * time + 0.5 * old->obj.rolling_ball.acc.y * time * time;
}

/**
 * @brief Checks whether a ROLLING_BALL has stopped, if it has converts it to a STILL_BALL. Assignment
 * allows us to assume 'object' is a ROLLING_BALL. Ball is considered stoped if it's speed is less then PHYLIB_VEL_EPSILON
 * Returns 1 if the ball is converted. Otherwise, returns 0.
 * @param object 
 * @return unsigned char 
 */
unsigned char phylib_stopped(phylib_object *object) {
    //Check that the object is not NULL and is NOT already a still ball. If not return.
    if (object == NULL || object->type != PHYLIB_ROLLING_BALL) {
        return 0; 
    }

    //Calculate the speed of the ball with equals length of the velocity
    double speed = phylib_length(object->obj.rolling_ball.vel); //Calculate the speed (length of the velocity)

    //Check if speed is less then PHYLIB_VEL_EPSILON (meaning it has stopped)
    if (speed < PHYLIB_VEL_EPSILON) {
        //Convert to STILL_BALL and reset all the properties (vel and acc)
        object->type = PHYLIB_STILL_BALL;
        object->obj.rolling_ball.vel.x = 0;
        object->obj.rolling_ball.vel.y = 0;
        object->obj.rolling_ball.acc.x = 0;
        object->obj.rolling_ball.acc.y = 0;

        return 1; //Meaning the ball stopped and has successfully converted
    }

    return 0; //If this is reached that means the ball was not slowed down enough to be considered stopped
}

/**
 * @brief Based on the type of object b (**b), handle the collision physics for each object type.
 * Assignment assumes object a (**a) is a ROLLING_BALL
 * @param a @param b 
 */
void phylib_bounce(phylib_object **a, phylib_object **b) {
    phylib_coord r_ab, v_rel;
    unsigned char old_number;
    //Check that the objects are not NULL or not ROLLING_BALL's. If so return.
    if (a == NULL || *a == NULL | (*a)->type != PHYLIB_ROLLING_BALL) {
        return;
    }

    //Switch case for handling collisions with object b based on object b's type
    switch((*b)->type) {
        //If object b is a Horizontal Cushion
        case PHYLIB_HCUSHION:
            //Negate (sign change) the y values of velocity and acceleration
            (*a)->obj.rolling_ball.vel.y = (-1 * (*a)->obj.rolling_ball.vel.y);
            (*a)->obj.rolling_ball.acc.y = (-1 * (*a)->obj.rolling_ball.acc.y);
            break;

        //If object b is a Vertical Cushion
        case PHYLIB_VCUSHION:
            //Negate (sign change) the x values of velocity and acceleration
            (*a)->obj.rolling_ball.vel.x = (-1 * (*a)->obj.rolling_ball.vel.x);
            (*a)->obj.rolling_ball.acc.x = (-1 * (*a)->obj.rolling_ball.acc.x);
            break;

        //If object b is a hole
        case PHYLIB_HOLE:
            free(*a); //Free the memory of a
            *a = NULL; //Set it to NULL
            break;

        //If object b is a Still Ball
        case PHYLIB_STILL_BALL:
            old_number = (*b)->obj.still_ball.number; //Store the ball number to apply to the new ROLLING_BALL
            phylib_coord original_coord = (*b)->obj.still_ball.pos; //Store the starting position of the STILL_BALL
            phylib_coord vel, acc;
            //Initialize the velocities and acceleration's to 0 
            vel.x = 0;
            acc.x = 0;
            vel.y = 0;
            acc.x = 0;
            free(*b); //Free the original STILL_BALL memory (get rid of it)
            (*b) = phylib_new_rolling_ball(old_number, &original_coord, &vel, &acc); //Create a ROLLING_BALL with the same properties
            //Automatically proceed to case 5 (no break statement)

        case PHYLIB_ROLLING_BALL:
            //Calculate the position of a relative to b. Call it r_ab. r_ab = r_a - r_b
            r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);

            //Calculate the velocity of a with respect to b. Call it v_rel
            v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);

            //Length of r_ab. Used for next step
            double r_ab_length = phylib_length(r_ab);
            //Divide the x and y components of r_ab by the length of r_ab. Call it n
            phylib_coord n = {r_ab.x / r_ab_length, r_ab.y / r_ab_length};

            //Ratio of the relative velocity v_rel by computing dot product of v_rel with respect to n. Call it v_rel_n
            double v_rel_n = phylib_dot_product(v_rel, n);

            phylib_coord v_a, v_b; //Variables used for updating and storing new velocities

            //Update the x velocity of ball a by subtracting v_rel * n.x (x component of vector n)
            v_a.x = (*a)->obj.rolling_ball.vel.x - v_rel_n * n.x;
            //Same for the y velocity
            v_a.y = (*a)->obj.rolling_ball.vel.y - v_rel_n * n.y;

            //Now update the x velocity of ball b by adding the product of v_rel and vector n
            v_b.x = (*b)->obj.rolling_ball.vel.x + v_rel_n * n.x;
            //Same for y velocity
            v_b.y = (*b)->obj.rolling_ball.vel.y + v_rel_n * n.y;

            //Now update the new velocities
            (*a)->obj.rolling_ball.vel = v_a;
            (*b)->obj.rolling_ball.vel = v_b;

            //Compute the speeds of a and b as the lengths of their velocities
            double speed_a = phylib_length((*a)->obj.rolling_ball.vel);
            double speed_b = phylib_length((*b)->obj.rolling_ball.vel);

            //If speed > PHYLIB_VEL_EPSILON then set acceleration to the negative velocity divided by speed * PHYLIB_DRAG
            if (speed_a > PHYLIB_VEL_EPSILON) {
                (*a)->obj.rolling_ball.acc.x = -((*a)->obj.rolling_ball.vel.x / speed_a) * PHYLIB_DRAG;
                (*a)->obj.rolling_ball.acc.y = -((*a)->obj.rolling_ball.vel.y / speed_a) * PHYLIB_DRAG;
            } 
            if (speed_b > PHYLIB_VEL_EPSILON) {
                (*b)->obj.rolling_ball.acc.x = -((*b)->obj.rolling_ball.vel.x / speed_b) * PHYLIB_DRAG;
                (*b)->obj.rolling_ball.acc.y = -((*b)->obj.rolling_ball.vel.y / speed_b) * PHYLIB_DRAG;
            } 
    }
}

/**
 * @brief Returns the number of ROLLING_BALLS on the table
 * @param t 
 * @return unsigned char 
 */
unsigned char phylib_rolling(phylib_table *t) {
    //Check that the table pointer is not NULL
    if (t == NULL) {
        return 0;
    }

    unsigned char rolling; //Initialize a variable to count the number of rolling balls
    rolling = 0; //Set it to 0

    //Iterate through the entire table and locate each rolling ball
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        //Check if the current object is not NULL and is a ROLLING_BALL
        if (t->object[i] != NULL && t->object[i]->type == PHYLIB_ROLLING_BALL) {
            rolling++; //Increment rolling by 1
        }
    }
    return rolling; //Return number of rolling balls found in table
}

/**
 * @brief Returns a segment of a pool shot. If there are no ROLLING_BALL's on the table, return NULL.
 * Otherwise, return a copy of the table. The returned table should be the result of applying phylib_roll()
 * to each ROLLING_BALL with time starting at PHYLIB_SIM_RATE. All balls must roll at the same time. 
 * The loop over time ends if PHYLIB_MAX_TIME is reached, if a ROLLING_BALL has stopped or if the distance 
 * between the ball and another object is less than 0.0 (meaning they collided), in which case apply phylib_bounce()
 * @param table 
 * @return phylib_table* 
 */
phylib_table *phylib_segment(phylib_table *table) {
    //Check if the table is NULL or if the table has no ROLLING_BALL's. If so return NULL.
    if(table == NULL || phylib_rolling(table) == 0) {
        return NULL;
    }

    phylib_table *copyTable = phylib_copy_table(table); //Create a copy of the table
    //Check if the copy was successful. If not return NULL
    if (copyTable == NULL) {
        return NULL;
    }

    double time = PHYLIB_SIM_RATE; //Set inital time to PHYLIB_SIM_RATE

    //Simulate the table for each time increment until MAX_TIME is reached
    for ( ; time <= PHYLIB_MAX_TIME; time += PHYLIB_SIM_RATE) {
        //Iterate over each object in the table
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
            phylib_object *current = copyTable->object[i]; //Store current object in 'current' 
            //If object in 'current' not NULL and is a ROLLING_BALL
            if (current != NULL && current->type == PHYLIB_ROLLING_BALL) {
                phylib_roll(current, table->object[i], time); // Apply roll to the rolling balls
            }
        }

        //Check for stopping conditions and collisions after rolling the balls
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
            phylib_object *current = copyTable->object[i];
            if (current != NULL && current->type == PHYLIB_ROLLING_BALL) {
                // Check if the ball has stopped
                if (phylib_stopped(current)) {
                    current->type = PHYLIB_STILL_BALL; //If stopped, change its type to STILL_BALL
                    copyTable->time += time;
                    return copyTable; //Return the updated table
                }
            }

            //Check for collisions with other objects
            for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++) {
                if (j != i && copyTable->object[j] != NULL) {
                    double distance = phylib_distance(current, copyTable->object[j]);
                    //If a collision is detected, apply phylib_bounce() 
                    if (distance < 0.0 && distance != -1.0) {
                        phylib_bounce(&(copyTable->object[i]), &(copyTable->object[j]));
                        copyTable->time += time;
                        return copyTable; //Return the updated table
                    }
                }
            }
        }
    }
    // Update the simulation time
    time += PHYLIB_SIM_RATE;
    copyTable->time += time;
    return copyTable; //Return the final table after simulation is complete
}

//A2: New Function in the A2 Description

char *phylib_object_string( phylib_object *object ) {
    static char string[80];
    if (object==NULL) {
        sprintf( string, "NULL;" );
        return string;
    }
    switch (object->type) {
        case PHYLIB_STILL_BALL:
            sprintf( string, "STILL_BALL (%d,%6.1lf,%6.1lf)", 
                    object->obj.still_ball.number, 
                    object->obj.still_ball.pos.x, 
                    object->obj.still_ball.pos.y );
            break;
        case PHYLIB_ROLLING_BALL:
            sprintf( string, "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)", 
                    object->obj.rolling_ball.number, 
                    object->obj.rolling_ball.pos.x, 
                    object->obj.rolling_ball.pos.y, 
                    object->obj.rolling_ball.vel.x, 
                    object->obj.rolling_ball.vel.y, 
                    object->obj.rolling_ball.acc.x, 
                    object->obj.rolling_ball.acc.y );
            break;
        case PHYLIB_HOLE:
            sprintf( string, "HOLE (%6.1lf,%6.1lf)", 
                    object->obj.hole.pos.x, 
                    object->obj.hole.pos.y );
            break;
        case PHYLIB_HCUSHION:
            sprintf( string, "HCUSHION (%6.1lf)", 
                    object->obj.hcushion.y );
            break;
        case PHYLIB_VCUSHION:
            sprintf( string, "VCUSHION (%6.1lf)", 
                    object->obj.vcushion.x );
            break;
    }
    return string;
}
