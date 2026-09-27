(define (problem blocks-7)
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
    (ontable d)
    (on e g)
    (on g b)
    (on b a)
    (on a f)
    (on f c)
    (on c d)
    (clear e)
    (handempty)
  )
  (:goal
    (and
      (on a g)
      (on g d)
      (on d b)
      (on b c)
      (on c f)
      (on f e)
    )
  )
)
