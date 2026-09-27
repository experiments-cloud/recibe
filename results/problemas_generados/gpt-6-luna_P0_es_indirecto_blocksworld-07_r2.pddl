(define (problem bloques)
  (:domain BLOCKS)
  (:objects
    a - block
    b - block
    c - block
    d - block
    e - block
    f - block
    g - block
  )
  (:init
    (on a d)
    (ontable d)
    (clear a)
    (on b c)
    (on c g)
    (on g e)
    (on e f)
    (ontable f)
    (clear b)
    (handempty)
  )
  (:goal
    (and
      (on e b)
      (on b f)
      (on f d)
      (on d a)
      (on a c)
      (on c g)
    )
  )
)
