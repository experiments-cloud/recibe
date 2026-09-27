(define (problem blocks-problem)
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
    (on e f)
    (on g e)
    (on c g)
    (on b c)
    (ontable f)
    (clear a)
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
