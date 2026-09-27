(define (problem bloques)
  (:domain BLOCKS)
  (:objects
    a - block
    b - block
    c - block
    d - block
    e - block
    f - block
  )
  (:init
    (on e b)
    (on f e)
    (ontable b)
    (clear f)
    (on a c)
    (on d a)
    (ontable c)
    (clear d)
    (handempty)
  )
  (:goal
    (and
      (on c b)
      (on b a)
      (on a e)
      (on e f)
      (on f d)
    )
  )
)
