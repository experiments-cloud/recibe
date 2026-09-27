(define (problem blocks-tower)
  (:domain BLOCKS)
  (:objects
    a - block
    b - block
    c - block
    d - block
    e - block
    f - block
    g - block
    h - block
    i - block
  )
  (:init
    (ontable a)
    (on h a)
    (on g h)
    (on i g)
    (on c i)
    (on d c)
    (on b d)
    (on e b)
    (on f e)
    (clear f)
    (handempty)
  )
  (:goal
    (and
      (on d i)
      (on i a)
      (on a b)
      (on b h)
      (on h g)
      (on g f)
      (on f e)
      (on e c)
    )
  )
)
