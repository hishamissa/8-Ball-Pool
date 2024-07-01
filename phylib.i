/******************************************************************************/
/* File:  phylib.i                                                            */
/******************************************************************************/
/* (C) Stefan C. Kremer, 2024                                                 */
/* A swig file to interface Python with the phylib library used for CIS*2750, */
/* Winter 2024.                                                               */
/******************************************************************************/

/* based on phylib.c and phylib.h */
%module phylib
%{
  #include "phylib.h"
%}

/******************************************************************************/

%include "phylib.h"

/******************************************************************************/
/* this creates a phylib_coord class in the phylib python module              */
/******************************************************************************/

%extend phylib_coord {

  /* constructor method */
  phylib_coord( double x, double y )
  {
    phylib_coord *new;
    new = malloc( sizeof( phylib_coord ) );
    new->x = x;
    new->y = y;
    return  new;
  }

  /* destructor method */
  ~phylib_coord()
  {
    free( $self );
  }
}

/******************************************************************************/
/* this creates a phylib_object class in the phylib python module             */
/******************************************************************************/

%extend phylib_object {

  /* constructor method */
  phylib_object( phylib_obj type, 
                 unsigned char num, 
                 phylib_coord *pos,
                 phylib_coord *vel,
                 phylib_coord *acc,
                 double x,
                 double y )
  {
    phylib_object *new;

    switch( type )
    {
      case PHYLIB_STILL_BALL:
        new = phylib_new_still_ball( num, pos );
        break;
      case PHYLIB_ROLLING_BALL:
        new = phylib_new_rolling_ball( num, pos, vel, acc );
        break;
      case PHYLIB_HOLE:
        new = phylib_new_hole( pos );
        break;
      case PHYLIB_HCUSHION:
        new = phylib_new_hcushion( y );
        break;
      case PHYLIB_VCUSHION:
        new = phylib_new_vcushion( x );
        break;
      default:
        PyErr_SetString( PyExc_ValueError, "bad type" );
        return NULL;
    } 
 
    if (!new)
    {
      PyErr_SetString( PyExc_ValueError, "malloc error" );
      return NULL;
    }
    return new;

  }

  /* __str__ method */
  PyObject* __str__()
  {
    char *str = phylib_object_string( $self );
    return PyString_FromString( str );
  }

  /* destructor method */
  ~phylib_object()
  {
    free( $self );
  }

}


/******************************************************************************/

%extend phylib_table {

  /****************************************************************************/

  /* constructor methods that calls new array */
  phylib_table()
  {
    return phylib_new_table();
  }

  /****************************************************************************/

  phylib_table *copy()
  {
    phylib_table *ptr = phylib_copy_table( $self );
    if (!ptr)
    {
      PyErr_SetString( PyExc_ValueError, "malloc error" );
      return NULL;
    }
    return ptr;
  }

  /****************************************************************************/

  phylib_table *segment()
  {
    return phylib_segment( $self );
  }

  /****************************************************************************/

  phylib_object *get_object( unsigned char i )
  {
    return $self->object[i];
  }

  /****************************************************************************/

  void add_object( phylib_object *object1 )
  {
    phylib_object *ptr;

    phylib_copy_object( &ptr, &object1 );
    phylib_add_object( self, ptr );
  }

  /****************************************************************************/

  /* free Array structure */
  ~phylib_table()
  {
    phylib_free_table( $self );
  }
};
