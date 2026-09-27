(define (problem blocks-6)
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
    (ontable b)
    (ontable c)
    (on f e)
    (on e b)
    (on d a)
    (on a c)
    (clear f)
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
