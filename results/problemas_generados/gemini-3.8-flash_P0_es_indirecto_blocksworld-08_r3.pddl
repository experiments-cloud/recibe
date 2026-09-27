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
    h - block
    i - block
  )
  (:init
    (handempty)
    (clear f)
    (on f e)
    (on e b)
    (on b d)
    (on d c)
    (on c i)
    (on i g)
    (on g h)
    (on h a)
    (ontable a)
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
